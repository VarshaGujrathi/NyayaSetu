from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('legal-simplifier/', views.legal_simplifier, name='legal_simplifier'),
    path('clause-risk-indicator/', views.clause_risk_indicator, name='clause_risk_indicator'),
    path('voice_text_interaction/', views.voice_text_interaction, name='voice_text_interaction'),
    path("compliance-alerts/", views.compliance_alerts, name="compliance_alerts"),
    path("smart-form-autofill/",views.smart_form_autofill,name="smart_form_autofill"),
    path("document-comparison/",views. document_comparison, name='document_comparison'),

]

