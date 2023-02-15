from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    # path('manage_user/', views.manage_user, name='manage_user'),
    # path('edit_user/<str:info_id>/', views.edit_user, name='edit_user'),
    # path('edit_user_info/<int:info_id>/', views.edit_user_info, name='edit_user_info'),
    # path('search/', views.search_user, name='search_user'),
]
