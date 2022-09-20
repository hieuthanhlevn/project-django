from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LOGIN, name='login'),
    path('register', views.REGISTER, name='register'),
    path('logout', views.LOGOUT, name='logout'),

    path('activate/<uidb64>/<token>/', views.ACTIVATE, name='activate'),
    path('forgotPassword/', views.FORGOT_PASSWORD, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.RESETPASSWORD_VALIDATE, name='resetpassword_validate'),
    path('resetPassword/', views.RESET_PASSWORD, name='resetPassword'),


    path('user/', views.MY_ACCOUNT, name='my_account'),
    path('user/my-orders/', views.MY_ORDERS, name='my_orders'),
    path('user/my-orders/detail/<int:id>', views.ORDERS_DETAIL, name='orders_detail'),
    path('user/edit-profile/', views.EDIT_PROFILE, name='edit_profile'),
    path('user/change_password/', views.CHANGE_PASSWORD, name='change_password'),

]
