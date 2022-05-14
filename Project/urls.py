
from django.urls import path, include
from .views import Project

urlpatterns = [
    path('', Project.as_view() ),
]