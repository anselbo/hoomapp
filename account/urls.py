from django.urls import path
from django.contrib.auth import views as auth_views # For importing my class base view from django default class base view, if not, its will not work
from . import views   # For my own define views
from .views import CustomizePasswordChangeView, CustomizePasswordResetView, CustomizePasswordResetDoneView # For importing my class base view that i subclass from django default class base view, if not, its will not work

"""Take note of these template:
    password_reset.html
    password_reset_set.html
    password_reset_done.html
"""

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('passwords_change/', CustomizePasswordChangeView.as_view(), name='passwords_change'),
    path('passwords_reset/', CustomizePasswordResetView.as_view(), name='passwords_reset'),
    path('passwords_reset/done/', CustomizePasswordResetDoneView.as_view(), name='passwords_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'account/passwords_reset_complete.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/passwords_reset_done_and_dusted.html'), name='password_reset_complete'),
    path('password_set/', views.password_set, name='password_set'),
    path('admin_change_user_password/<int:pk>/', views.admin_change_user_password, name='admin_change_user_password'),
    path('admin_register_user/', views.admin_register_user, name='admin_register_user'),


    path('all_users/', views.all_users, name='all_users'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('detail_for_admin/<int:pk>/', views.detail_for_admin, name='detail_for_admin'),
    path('user_wear/<int:pk>/', views.user_wear, name='user_wear'),
    path('all_wears_from_all_users/', views.all_wears_from_all_users, name='all_wears_from_all_users'),
    # path('passwords_reset/<uidb64>/<token>/', CustomizePasswordResetCompleteView.as_view(), name='password_reset_confirm'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'), # default password change view
    # path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
]