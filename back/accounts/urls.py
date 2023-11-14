from knox import views as knox_views
from .views import (
    UserAPI,
    LoginAPI,
    RegisterAPI,
    UserDetailAPI,
    UserUpdateAPI,
    UserDeleteAPI,
    # ValidateOTP,
    # LoginWithOTP,
    ChangePasswordView,
    PersonView,
)
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('user/', UserAPI.as_view(), name='user'),
    path('user/detail/<int:pk>/', UserDetailAPI.as_view(), name='user_detail'),
    path('user/update/<int:pk>/', UserUpdateAPI.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDeleteAPI.as_view(), name='user_delete'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('persons/', PersonView.as_view(), name='persons'), 
    # path('login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    # path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
]