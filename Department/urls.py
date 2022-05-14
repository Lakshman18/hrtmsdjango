
from django.urls import path, include
from .views import departments

urlpatterns = [
    path('', departments.as_view() ),
]