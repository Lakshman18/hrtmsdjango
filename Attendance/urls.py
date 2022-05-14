
from django.urls import path, include
from .views import attendance

urlpatterns = [
    path('', attendance.as_view() ),
]