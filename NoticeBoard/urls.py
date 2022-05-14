
from django.urls import path, include
from .views import noticeboard

urlpatterns = [
    path('', noticeboard.as_view() ),
]