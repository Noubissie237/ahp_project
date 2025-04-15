import numpy as np
from .models import CriteriaComparison, AlternativeScore

class AHPCalculator:
    def __init__(self, criteria, alternatives, criteria_comparison, performance_matrix):
        self.criteria = criteria
        self.alternatives = alternatives
        self.criteria_comparison = np.array(criteria_comparison)
        self.performance_matrix = np.array(performance_matrix)
    
    @classmethod
    def from_database(cls, matrix_id):
        # Récupérer les comparaisons de critères
        criteria_comps = CriteriaComparison.objects.filter(matrix_id=matrix_id)
        criteria = list(set([comp.criteria1.name for comp in criteria_comps] + 
                          [comp.criteria2.name for comp in criteria_comps]))
        criteria.sort()
        
        # Construire la matrice de comparaison
        n = len(criteria)
        criteria_comparison = np.ones((n, n))
        
        for comp in criteria_comps:
            i = criteria.index(comp.criteria1.name)
            j = criteria.index(comp.criteria2.name)
            criteria_comparison[i][j] = comp.value
            criteria_comparison[j][i] = 1 / comp.value
        
        # Récupérer les scores des alternatives
        alt_scores = AlternativeScore.objects.filter(matrix_id=matrix_id)
        alternatives = list(set([score.alternative.name for score in alt_scores]))
        alternatives.sort()
        
        performance_matrix = np.zeros((len(alternatives), len(criteria)))
        
        for score in alt_scores:
            i = alternatives.index(score.alternative.name)
            j = criteria.index(score.criteria.name)
            performance_matrix[i][j] = score.score
        
        return cls(criteria, alternatives, criteria_comparison, performance_matrix)
    
    def calculate_weights(self, comparison_matrix):
        n = comparison_matrix.shape[0]
        geometric_means = np.prod(comparison_matrix, axis=1) ** (1/n)
        weights = geometric_means / geometric_means.sum()
        return weights
    
    def calculate_consistency(self, comparison_matrix, weights):
        n = comparison_matrix.shape[0]
        lambda_max = np.sum((comparison_matrix @ weights) / weights) / n
        ci = (lambda_max - n) / (n - 1)
        ri = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
        cr = ci / ri[n-1] if n-1 < len(ri) else 0
        return cr
    
    def normalize_performance(self):
        max_values = self.performance_matrix.max(axis=0)
        min_values = self.performance_matrix.min(axis=0)
        
        normalized = np.zeros_like(self.performance_matrix, dtype=float)
        
        for i in range(self.performance_matrix.shape[1]):
            if any(term in self.criteria[i].lower() for term in ['price', 'prix']):  # Moins est mieux
                normalized[:, i] = min_values[i] / self.performance_matrix[:, i]
            else:  # Plus est mieux
                normalized[:, i] = self.performance_matrix[:, i] / max_values[i]
                
        return normalized
    
    def calculate(self):
        # Calculer les poids des critères
        criteria_weights = self.calculate_weights(self.criteria_comparison)
        
        # Vérifier la cohérence
        cr = self.calculate_consistency(self.criteria_comparison, criteria_weights)
        
        # Normaliser la matrice de performance
        normalized_performance = self.normalize_performance()
        
        # Calculer les scores finaux
        final_scores = normalized_performance @ criteria_weights
        
        # Associer les scores aux alternatives
        ranked_alternatives = list(zip(self.alternatives, final_scores))
        ranked_alternatives.sort(key=lambda x: x[1], reverse=True)
        
        return {
            'criteria_weights': dict(zip(self.criteria, criteria_weights)),
            'consistency_ratio': cr,
            'ranked_alternatives': ranked_alternatives,
            'best_choice': ranked_alternatives[0] if ranked_alternatives else None
        }