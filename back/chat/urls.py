from django.urls import path
from .views import *

urlpatterns = [
    path('api/', chat),
    path('api/chat/', ChatView.as_view()),
]