
from django.urls import path, include
from .views import vacancy, application

urlpatterns = [
    path('', vacancy.as_view() ),
    path('application', application.as_view() ),
]