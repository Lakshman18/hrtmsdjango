
from django.urls import path, include
from .views import roles,Register,Login,EmpView,Logout,viewAllEmp, PwdChange, pictureChange

urlpatterns = [
    path('roles', roles.as_view() ),
    path('register', Register.as_view() ),
    path('login', Login.as_view() ),
    path('EmpView', EmpView.as_view() ),
    path('logout', Logout.as_view() ),
    path('viewAllEmp', viewAllEmp.as_view() ),
    path('PwdChange', PwdChange.as_view() ),
    path('pictureChange', pictureChange.as_view() ),
]