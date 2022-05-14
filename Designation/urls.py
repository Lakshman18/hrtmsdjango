
from django.urls import path, include
from .views import designation

urlpatterns = [
    path('', designation.as_view() ),
]