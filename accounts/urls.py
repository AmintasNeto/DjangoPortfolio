from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('createOrder/', views.createOrder, name="createOrder"),
    path('updateOrder/<str:pk>', views.updateOrder, name="updateOrder"),
    path('deleteOrder/<str:pk>', views.deleteOrder, name="deleteOrder"),
    path('createCustomer/', views.createCustomer, name="createCustomer"),
    path('updateCustomer/<str:pk>', views.updateCustomer, name="updateCustomer"),
    path('deleteCustomer/<str:pk>', views.deleteCustomer, name="deleteCustomer"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.register, name="register"),
    path('user/', views.userPage, name="user"),
    path('settings/', views.accountSettingPage, name="settings"),

    path('resetPassword/', auth_views.PasswordResetView.as_view(template_name='accounts/passwordReset.html'),
         name="reset_password"),

    path('resetPasswordSent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/paswordResetSent.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/paswordResetForm.html'),
         name="password_rese_confirm"),

    path('resetPasswordCompleted/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/paswordResetDone.html'),
         name="password_reset_complete"),
]
