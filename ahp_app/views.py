from django.shortcuts import render, redirect
from django.views import View
from .models import Criteria, Alternative, ComparisonMatrix, CriteriaComparison, AlternativeScore
from .ahp_calculator import AHPCalculator
import numpy as np
from django.contrib import messages

class HomeView(View):
    def get(self, request):
        return render(request, 'pages/home.html')

class QuickModeView(View):
    def get(self, request):
        # Données statiques pour l'exercice du cours
        static_data = {
            'criteria': ['Memory', 'Storage', 'CPU Frequency', 'Price', 'Brand'],
            'alternatives': [
                'Iphone 12', 'ItelA56', 'Tecno Camon 12', 'Infinix Hot 10',
                'Huawei P30', 'Google Pixel 7', 'Xiaomi Redmi note 10',
                'Samsung Galaxy S22', 'Motorola razr+', 'Iphone X R',
                'Samsung Galaxy Note 10'
            ],
            'criteria_comparison': [
                [1, 3, 2, 5, 4],
                [1/3, 1, 1/2, 3, 2],
                [1/2, 2, 1, 4, 3],
                [1/5, 1/3, 1/4, 1, 1/2],
                [1/4, 1/2, 1/3, 2, 1]
            ],
            'performance_matrix': [
                [8, 128, 2.7, 458500, 9],
                [2, 32, 1.3, 52400, 4],
                [4, 64, 1.8, 98250, 5],
                [4, 64, 2.0, 78600, 5],
                [6, 128, 2.3, 262000, 7],
                [8, 128, 2.8, 393000, 8],
                [6, 128, 2.2, 117900, 6],
                [8, 256, 3.0, 524000, 9],
                [8, 256, 2.9, 655000, 7],
                [6, 64, 2.5, 327500, 8],
                [8, 256, 2.8, 491250, 9]
            ]
        }
        
        calculator = AHPCalculator(
            static_data['criteria'],
            static_data['alternatives'],
            static_data['criteria_comparison'],
            static_data['performance_matrix']
        )
        
        results = calculator.calculate()
        
        context = {
            'criteria': static_data['criteria'],
            'alternatives': static_data['alternatives'],
            'results': results,
            'mode': 'quick'
        }
        
        return render(request, 'pages/results.html', context)

class CustomModeView(View):
    def get(self, request):
        return render(request, 'pages/custom_mode.html')
    
    def post(self, request):
        criteria = request.POST.getlist('criteria')
        alternatives = request.POST.getlist('alternatives')
        
        matrix = ComparisonMatrix.objects.create(name="Custom AHP Analysis")
        
        for crit in criteria:
            Criteria.objects.get_or_create(name=crit)
        
        for alt in alternatives:
            Alternative.objects.get_or_create(name=alt)
        
        request.session['matrix_id'] = matrix.id
        request.session['criteria'] = criteria
        request.session['alternatives'] = alternatives
        
        return redirect('criteria_comparison')

class CriteriaComparisonView(View):
    def get(self, request):
        criteria = request.session.get('criteria', [])
        context = {
            'criteria': criteria,
            'matrix_id': request.session.get('matrix_id')
        }
        return render(request, 'pages/criteria_comparison.html', context)
    
    def post(self, request):
        matrix_id = request.session.get('matrix_id')
        criteria = request.session.get('criteria', [])
        alternatives = request.session.get('alternatives', [])
        
        try:
            matrix = ComparisonMatrix.objects.get(id=matrix_id)
        except ComparisonMatrix.DoesNotExist:
            return redirect('home')
        
        # Enregistrer les comparaisons par paires avec validation
        for i, crit1 in enumerate(criteria):
            for j, crit2 in enumerate(criteria[i+1:], start=i+1):
                value_str = request.POST.get(f'compare_{i}_{j}')
                if not value_str:  # Si la valeur est None ou chaîne vide
                    messages.error(request, f"Veuillez sélectionner une valeur pour la comparaison entre {crit1} et {crit2}")
                    return self.get(request)  # Re-afficher le formulaire avec l'erreur
                
                try:
                    value = float(value_str)
                except ValueError:
                    messages.error(request, f"Valeur invalide pour la comparaison entre {crit1} et {crit2}")
                    return self.get(request)
                
                crit1_obj, _ = Criteria.objects.get_or_create(name=crit1)
                crit2_obj, _ = Criteria.objects.get_or_create(name=crit2)
                
                CriteriaComparison.objects.create(
                    matrix=matrix,
                    criteria1=crit1_obj,
                    criteria2=crit2_obj,
                    value=value
                )
        
        return redirect('alternative_scores')

class AlternativeScoresView(View):
    def get(self, request):
        criteria = request.session.get('criteria', [])
        alternatives = request.session.get('alternatives', [])
        
        context = {
            'criteria': criteria,
            'alternatives': alternatives,
            'matrix_id': request.session.get('matrix_id')
        }
        return render(request, 'pages/alternative_scores.html', context)
    
    def post(self, request):
        matrix_id = request.session.get('matrix_id')
        criteria = request.session.get('criteria', [])
        alternatives = request.session.get('alternatives', [])
        
        matrix = ComparisonMatrix.objects.get(id=matrix_id)
        
        # Enregistrer les scores des alternatives
        for i, alt in enumerate(alternatives):
            for j, crit in enumerate(criteria):
                score = float(request.POST.get(f'score_{i}_{j}'))
                alt_obj = Alternative.objects.get(name=alt)
                crit_obj = Criteria.objects.get(name=crit)
                
                AlternativeScore.objects.create(
                    matrix=matrix,
                    alternative=alt_obj,
                    criteria=crit_obj,
                    score=score
                )
        
        # Calculer les résultats
        calculator = AHPCalculator.from_database(matrix_id)
        results = calculator.calculate()
        
        context = {
            'criteria': criteria,
            'alternatives': alternatives,
            'results': results,
            'mode': 'custom'
        }
        
        return render(request, 'pages/results.html', context)