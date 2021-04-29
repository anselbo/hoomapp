from django.contrib import admin
from .models import WearCategory, Wear, FinanceCategory, Finance, Task, TaskCategory

@admin.register(WearCategory)
class WearCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_owner', 'category_name', 'date_created', 'date_updated', 'activate']
    # prepopulated_fields = {'slug': ('name',)}
    


@admin.register(Wear)
class WearAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'category', 'amount', 'bought_from', 'date_created', 'date_updated', 
    'activate']
    # prepopulated_fields = {'slug': ('name',)}
    

@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'category', 'amount', 'date_created', 'date_updated', 
    'activate']


@admin.register(FinanceCategory)
class FinanceCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_owner', 'category_name', 'date_created', 'date_updated', 
    'activate']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'complete', 'date_created', 'date_updated', 'due', 'activate']

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'date_created', 'date_updated', 'activate']