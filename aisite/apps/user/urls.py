from django.urls import path
from .views import SignupView, SigninView, logout, UserExist

urlpatterns = [
    path('register/', SignupView.as_view(), name='register'),
    path('login/', SigninView.as_view(), name='login'),
    path('userExist/', UserExist.as_view(), name='userExist'),
    path('logout/', logout, name='logout'),
]
