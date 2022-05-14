from django.urls import path, include
from .views import timesheet

urlpatterns = [
    path('', timesheet.as_view() ),
]