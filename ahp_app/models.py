from django.db import models

class Criteria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Alternative(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ComparisonMatrix(models.Model):
    name = models.CharField(max_length=100)
    criteria = models.ManyToManyField(
        Criteria, 
        through='CriteriaComparison',
        through_fields=('matrix', 'criteria1'), 
        related_name='comparison_matrices'
    )
    alternatives = models.ManyToManyField(
        Alternative, 
        through='AlternativeScore',
        related_name='comparison_matrices'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CriteriaComparison(models.Model):
    matrix = models.ForeignKey(ComparisonMatrix, on_delete=models.CASCADE)
    criteria1 = models.ForeignKey(
        Criteria, 
        related_name='first_criteria_comparisons',
        on_delete=models.CASCADE
    )
    criteria2 = models.ForeignKey(
        Criteria, 
        related_name='second_criteria_comparisons',
        on_delete=models.CASCADE
    )
    value = models.FloatField()

    class Meta:
        unique_together = ('matrix', 'criteria1', 'criteria2')

class AlternativeScore(models.Model):
    matrix = models.ForeignKey(ComparisonMatrix, on_delete=models.CASCADE)
    alternative = models.ForeignKey(Alternative, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    score = models.FloatField()

    class Meta:
        unique_together = ('matrix', 'alternative', 'criteria')