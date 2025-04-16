from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('quick-mode/', views.QuickModeView.as_view(), name='quick_mode'),
    path('custom-mode/', views.CustomModeView.as_view(), name='custom_mode'),
    path('criteria-comparison/', views.CriteriaComparisonView.as_view(), name='criteria_comparison'),
    path('alternative-scores/', views.AlternativeScoresView.as_view(), name='alternative_scores'),
    path('about/', views.about, name='about')
]