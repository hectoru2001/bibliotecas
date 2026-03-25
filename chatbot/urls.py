from django.urls import path
from . import views

app_name = 'chatbot'  # Define el namespace

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
]