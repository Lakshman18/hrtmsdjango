from django.urls import path, include
from .views import dashboard,test

urlpatterns = [
    path('', dashboard.as_view() ),
    path('test', test.as_view() ),
]