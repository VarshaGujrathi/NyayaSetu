from django.urls import path
from . import views

app_name = 'translator'

urlpatterns = [
    # This connects the homepage to your 'index' view
    path('', views.index, name='index'),
    
    # These are the API connections for your buttons
    path('api/translate/', views.translate_text, name='translate_text'),
    path('api/transcribe/', views.transcribe_audio, name='transcribe_audio'),
    path('api/speak/', views.synthesize_speech, name='synthesize_speech'),
]