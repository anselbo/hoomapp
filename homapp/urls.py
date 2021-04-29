from django.urls import path
from . import views  
from .views import WearDetailView, FinanceDetailView

app_name = 'homapp'

urlpatterns = [
    path('', views.wear_list, name='wears_list'),
    path('deactivated_wears/', views.deactivate_wears, name='deactivated_wears'),
    path('add_wear/', views.add_wear, name='register_wear'),
    path('<int:wear_category_id>/', views.wear_list, name='wears_list_by_category'),
    path('wear_detail/<int:pk>/', WearDetailView.as_view(), name='wear_detail'),
    path('delete_wear/<int:id>/', views.delete_wear, name='delete_wear'),
    path('update_wear/<int:pk>/', views.update_wear, name='update_wear'),
    path('add_category/', views.add_category, name='add_category'),
    path('category_list/', views.category_list, name='category_list'),
    path('edit_category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('deactivated_category/', views.deactivated_category, name='deactivated_category'),
    

    # path('<int:pk>/', views.wear_detail, name='wear_detail'),
    # path('register_clothe/', views.register_clothe, name='register_clothe'),
    # path('<slug:category_slug>/', views.clothe_list, name='clothes_list_by_category'),
    # path('<slug:slug>/<int:year>/<int:month>/<int:day>/<int:id>/', views.clothe_detail, name='clothe_detail'), 
    # path('delete_clothe/<int:id>/', views.delete_clothe, name='delete_clothe'),

    path('finance_list/', views.finance_list, name='finance_list'),
    path('finance_detail/<int:pk>/', FinanceDetailView.as_view(), name='finance_detail'),
    path('add_finance/', views.add_finance, name='add_finance'),
    path('edit_finance/<int:pk>/', views.edit_finance, name='edit_finance'),
    path('delete_finance/<int:pk>/', views.delete_finance, name='delete_finance'),
    path('finance_cat_list/', views.finance_cat_list, name='finance_cat_list'),
    path('add_fin_category/', views.add_fin_category, name='add_fin_category'),
    path('edit_fin_category/<int:pk>/', views.edit_fin_category, name='edit_fin_category'),
    path('delete_fin_category/<int:pk>/', views.delete_fin_category, name='delete_fin_category'),
    path('deactivated_finances/', views.deactivated_finances, name='deactivated_finances'),
    path('all_transactions/', views.all_transactions, name='all_transactions'),
    path('today_summary/', views.today_summary, name='today_summary'),
    path('last_3_days/', views.last_3_days, name='last_3_days'),
    path('last_7_days/', views.last_7_days, name='last_7_days'),
    path('current_week/', views.current_week, name='current_week'),
    path('current_month/', views.current_month, name='current_month'),
    path('current_year/', views.current_year, name='current_year'),
    path('deactivated_finance_category/', views.deactivated_finance_category, name='deactivated_finance_category'),
    path('finance_deactivated_edit_category/<int:pk>/', views.finance_deactivated_edit_category, name='finance_deactivated_edit_category'),
    path('edit_finance_deactivated/<int:pk>/', views.edit_finance_deactivated, name='edit_finance_deactivated'),
    path('delete_deactivated_finance/<int:pk>/', views.delete_deactivated_finance, name='delete_deactivated_finance'),
    path('delete_fin_deactivated_category/<int:pk>/', views.delete_fin_deactivated_category, name='delete_fin_deactivated_category'),


    # Todo task 
    path('list_task/', views.list_task, name='list_task'),
    path('update_task/<int:pk>/', views.update_todo_task, name='update_todo_task'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),
    path('task_detail/<int:pk>/', views.task_detail, name='task_detail'),
    path('list_task_category/', views.list_task_category, name='list_task_category'),
    path('update_task_category/<int:pk>/', views.update_task_category, name='update_task_category'),
    path('delete_task_category/<int:pk>/', views.delete_task_category, name='delete_task_category'),
    path('deactivated_task/', views.deactivated_task, name='deactivated_task'),
    path('update_todo_task_deactivated/<int:pk>', views.update_todo_task_deactivated, name='update_todo_task_deactivated'),
    path('deactivated_task_category/', views.deactivated_task_category, name='deactivated_task_category'),
    path('update_task_deactivated_category/<int:pk>/', views.update_task_deactivated_category, name='update_task_deactivated_category'),


    # for admin view only
    path('all_wears_for_admin/', views.all_wears_for_admin, name='all_wears_for_admin'),
]


