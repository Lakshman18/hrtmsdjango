from django.urls import path, include
from .views import Client, Login, ClientView, PwdChange

urlpatterns = [
    path('', Client.as_view() ),
    path('login', Login.as_view() ),
    path('ClientView', ClientView.as_view() ),
    path('PwdChange', PwdChange.as_view() ),
]