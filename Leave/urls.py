
from django.urls import path, include
from .views import leave

urlpatterns = [
    path('', leave.as_view() ),
]