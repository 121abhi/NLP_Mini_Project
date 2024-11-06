from django.urls import path
from . import views

urlpatterns = [
    path('linkedin_analysis/', views.analyze_linkedin, name='linkedin_analysis'),
]
