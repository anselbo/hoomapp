from django import template  
from ..models import Wear, Finance, Task
from datetime import datetime, date, timedelta
from django.utils import timezone  
from django.conf import settings 

register = template.Library()

@register.simple_tag
def count_all_today_data():
    today = date.today()
    today_wear_data = Wear.objects.filter(activate=True, date_created__date=today).count()
    today_finance_data = Finance.objects.filter(activate=True, date_created__date=today).count()
    count_today_data = today_wear_data + today_finance_data
    return count_today_data

@register.simple_tag
def count_last_3_days_data():
    today = timezone.now()
    last_3_days = today - timedelta(days=3)
    last_3_days_wear_data = Wear.objects.filter(activate=True, date_created__range=(last_3_days, today)).count()
    last_3_days_finance_data = Finance.objects.filter(activate=True, date_created__range=(last_3_days, today)).count()
    sum_all_last_3_days_data = last_3_days_wear_data + last_3_days_finance_data
    return sum_all_last_3_days_data


@register.simple_tag
def count_last_7_days_data():
    today = timezone.now()
    last_7_days = today - timedelta(days=7)
    last_7_days_wear_data = Wear.objects.filter(activate=True, date_created__range=(last_7_days, today)).count()
    last_7_days_finance_data = Finance.objects.filter(activate=True, date_created__range=(last_7_days, today)).count()
    sum_all_last_7_days_data = last_7_days_wear_data + last_7_days_finance_data
    return sum_all_last_7_days_data




@register.simple_tag
def count_current_week_data():
    current_date = timezone.now()
    current_year, current_week, current_weekday = current_date.isocalendar()  
    current_week_wear_data = Wear.objects.filter(activate=True, date_created__week=current_week).count()
    current_week_finance_data = Finance.objects.filter(activate=True, date_created__week=current_week).count()
    sum_all_current_week_data = current_week_wear_data + current_week_finance_data
    return sum_all_current_week_data



@register.simple_tag
def count_current_month_data():
    current_date = timezone.now()
    current_month = current_date.month  
    current_month_wear_data = Wear.objects.filter(activate=True, date_created__month=current_month).count()
    current_month_finance_data = Finance.objects.filter(activate=True, date_created__month=current_month).count()
    sum_all_current_month_data = current_month_wear_data + current_month_finance_data
    return sum_all_current_month_data



@register.simple_tag
def count_current_year_data():
    current_date = timezone.now()
    current_year = current_date.year  
    current_year_wear_data = Wear.objects.filter(activate=True, date_created__year=current_year).count()
    current_year_finance_data = Finance.objects.filter(activate=True, date_created__year=current_year).count()
    sum_all_current_year_data = current_year_wear_data + current_year_finance_data
    return sum_all_current_year_data


@register.simple_tag
def count_tasks():
    uncompleted_tasks = Task.objects.filter(activate=True, complete=False).count()
    return uncompleted_tasks




# @register.simple_tag
# def show_deactivated_wear(count=1):
#     deactivated_wears = Wear.objects.filter(activate=False).order_by('-date_created')[:count]
#     return deactivated_wears




@register.inclusion_tag('homapp/wears/latest_wears.html')
def show_latest_wear(count=1):
    latest_wears = Wear.objects.filter(activate=True).order_by('-date_created')[:count]
    return {'latest_wears': latest_wears}


# @register.inclusion_tag('homapp/wears/deactivated_wearss.html')
# def show_deactivated_wear(count=1):
#     deactivated_wears = Wear.objects.filter(activate=False).order_by('-date_created')[:count]
#     return {'deactivated_wears': deactivated_wears}



# @register.inclusion_tag('homapp/wears/deactivated_wears.html')
# def deactivate_wears(request):
#     deactivated_wears = Wear.objects.filter(activate=False)
#     return {'deactivated_wears': deactivate_wears}
