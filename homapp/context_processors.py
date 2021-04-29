from django.conf import settings
from .models import Task, TaskCategory, Finance, Wear
from datetime import datetime, date, time, timedelta
from django.utils import timezone

def uncompleted_tasks_context(request):
    uncompleted_tasks = Task.objects.filter(user_id=request.user.id, activate=True, complete=False).count()
    return {
        'uncompleted_tasks': uncompleted_tasks
    }




def count_all_today_data(request):
    today = date.today()
    today_wear_data = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__date=today).count()
    today_finance_data = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__date=today).count()
    count_today_data = today_wear_data + today_finance_data
    return {
        'count_today_data': count_today_data,
    }


def count_last_3_days_data(request):
    today = timezone.now()
    last_3_days = today - timedelta(days=3)
    last_3_days_wear_data = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_3_days, today)).count()
    last_3_days_finance_data = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_3_days, today)).count()
    sum_all_last_3_days_data = last_3_days_wear_data + last_3_days_finance_data
    return {
        'sum_all_last_3_days_data': sum_all_last_3_days_data,
    }



def count_last_7_days_data(request):
    today = timezone.now()
    last_7_days = today - timedelta(days=7)
    last_7_days_wear_data = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_7_days, today)).count()
    last_7_days_finance_data = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_7_days, today)).count()
    sum_all_last_7_days_data = last_7_days_wear_data + last_7_days_finance_data
    return {
        'sum_all_last_7_days_data': sum_all_last_7_days_data,
    }





def count_current_week_data(request):
    current_date = timezone.now()
    current_year, current_week, current_weekday = current_date.isocalendar()  
    current_week_wear_data = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__week=current_week).count()
    current_week_finance_data = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__week=current_week).count()
    sum_all_current_week_data = current_week_wear_data + current_week_finance_data
    return {
        'sum_all_current_week_data': sum_all_current_week_data,
    }




def count_current_month_data(request):
    current_date = timezone.now()
    current_month = current_date.month  
    current_month_wear_data = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__month=current_month).count()
    current_month_finance_data = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__month=current_month).count()
    sum_all_current_month_data = current_month_wear_data + current_month_finance_data
    return {
        'sum_all_current_month_data': sum_all_current_month_data,
    }




def count_current_year_data(request):
    current_date = timezone.now()
    current_year = current_date.year  
    current_year_wear_data = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__year=current_year).count()
    current_year_finance_data = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__year=current_year).count()
    sum_all_current_year_data = current_year_wear_data + current_year_finance_data
    return {
        'sum_all_current_year_data': sum_all_current_year_data,
    }


def footer_current_year(request):
    current_date = timezone.now()
    current_year = current_date.year
    return {
        'current_year': current_year,
    }