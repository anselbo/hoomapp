from django.shortcuts import render, redirect, get_object_or_404 
from .models import WearCategory, Wear, Finance, FinanceCategory, Task, TaskCategory
from django.db.models import Sum, DecimalField, Q, Value as V  
from django.db.models.functions import Coalesce
from .forms import AdminEditTaskCategoryForm, AdminEditWearCategoryForm, AdminAddWearCategoryForm, AdminFinanceCategoryEditForm, AdminAddFinanceCategoryForm, AdminEditWearForm,  AdminEditFinanceForm, AdminEditTaskForm, WearRegisterForm, EditFinanceDectForm, FinanceDeactivatedCatForm, WearEditForm, TaskCategoryForm, UpdateTaskCategoryForm, AddCategoryForm, CatEditForm,  CatSelectForm, FinCatSelectForm, FinanceAddForm, EditFinanceForm, AddFinanceCategoryForm, FinanceCatEditForm, TodoForm, UpdateTodoForm, AdminAddFinanceForm, AdminAddWearForm, AdminAddTaskForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import  DetailView
from .filters import WearFilter 
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from homapp_project.decorators import only_admin, unauthorized_user
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector



@login_required
def wear_list(request, song_cat=None, wear_category_id=None):

    # This is the one that am using now.....
    s_with_cat = None 
    selected_category = None
    count_with_data_selected = None

    categories = WearCategory.objects.filter(category_owner_id=request.user.id, activate=True)
    

    qs = Wear.objects.filter(user_id=request.user.id, activate=True)
    last_added_wear = Wear.objects.filter(user_id=request.user.id, activate=True)[:1]
    deactivated_wearss = Wear.objects.filter(user_id=request.user.id, activate=False).count()

    sum_all_n_wears = Wear.objects.filter(user_id=request.user.id, activate=True).aggregate(a=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # To sum all wears..
    sum_all_n_wears = sum_all_n_wears.get('a')

    # getting the names from the form
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = request.GET.get('expenses')
    not_expenses = request.GET.get('not_expenses')
    search = request.GET.get('search')

    
    if category != '' and category != None and category != 'Choose...':
        qs = qs.filter(category_id=category)
        count_with_data_selected = qs.filter(category_id=category)
        selected_category = get_object_or_404(WearCategory, id=category)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table

        # Suming amount based on the category selected
        selected_category = get_object_or_404(WearCategory, id=category, category_owner_id=request.user.id,)
        s_with_cat = qs.filter(category_id=category).aggregate(ba=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('ba')

       
    
    if start_date != '' and start_date != None:
        qs = qs.filter(date_created__gte=start_date)
        count_with_data_selected = qs.filter(date_created__gte=start_date)

        # Suming amount based on only the start date selected
        selected_category = qs.filter(date_created__gte=start_date)
        s_with_cat = qs.filter(date_created__gte=start_date).aggregate(baa=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('baa')
        

    if end_date != '' and end_date != None:
        qs = qs.filter(date_created__lt=end_date)
        count_with_data_selected = qs.filter(date_created__lt=end_date)

        # Suming amount based on only the end date selected
        selected_category = qs.filter(date_created__lt=end_date)
        s_with_cat = qs.filter(date_created__lt=end_date).aggregate(con=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('con')
    
    if search != '' and search != None: 
        qs = qs.filter(Q(name__icontains=search) | Q(amount__icontains=search) | Q(bought_from__icontains=search))
        count_with_data_selected = qs.filter(Q(name__icontains=search) | Q(amount__icontains=search) | Q(bought_from__icontains=search))

        # summing amount based on the word search on
        selected_category = qs.filter(Q(name__icontains=search) | Q(amount__icontains=search) | Q(bought_from__icontains=search))
        s_with_cat = qs.filter(Q(name__icontains=search) | Q(amount__icontains=search) | Q(bought_from__icontains=search)).aggregate(ho=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('ho')
    
    if expenses == 'on':
        qs = qs.filter(expenses=True)
        count_with_data_selected = qs.filter(expenses=True)
        
        # summing amount based on the expenses activated
        selected_category = qs.filter(expenses=True)
        s_with_cat = qs.filter(expenses=True).aggregate(ton=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('ton')

    elif not_expenses == 'on':
        qs = qs.filter(expenses=False)
        count_with_data_selected = qs.filter(expenses=False)

        
        # summing amount based on the expenses deactivated
        selected_category = qs.filter(expenses=False)
        s_with_cat = qs.filter(expenses=False).aggregate(tah=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('tah')  


    context = {
        'deactivated_wearss': deactivated_wearss,

        'qs': qs,
        'categories': categories,
        'sum_all_n_wears': sum_all_n_wears,
        's_with_cat': s_with_cat,
        'selected_category': selected_category,
        'count_with_data_selected': count_with_data_selected,
        'last_added_wear': last_added_wear,
        
        
       
        
           
    }
    return render(request, 'homapp/wears/list.html', context)



@login_required
def deactivate_wears(request, song_cat=None, wear_category_id=None):
    count_with_category = None
    selected_category = None
    s_with_cat = None

     # This is the one that am using now.....
    count_with_data_selected = None

    all_wear_categories = WearCategory.objects.filter(category_owner_id=request.user.id, activate=True)
    qs = Wear.objects.filter(user_id=request.user.id, activate=False)

    sum_all_d_wears = Wear.objects.filter(user_id=request.user.id, activate=False).aggregate(a=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # To sum all wears..
    sum_all_d_wears = sum_all_d_wears.get('a')

    # getting the names from the form
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = request.GET.get('expenses')
    not_expenses = request.GET.get('not_expenses')

    
    if category != '' and category != None and category != 'Choose...':
        qs = qs.filter(category_id=category)
        count_with_data_selected = qs.filter(category_id=category)
        selected_category = get_object_or_404(WearCategory, id=category, category_owner_id=request.user.id)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table

        # Suming amount based on the category selected
        selected_category = get_object_or_404(WearCategory, id=category)
        s_with_cat = qs.filter(category_id=category).aggregate(ba=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('ba')

       
    
    if start_date != '' and start_date != None:
        qs = qs.filter(date_created__gte=start_date)
        count_with_data_selected = qs.filter(date_created__gte=start_date)

        # Suming amount based on only the start date selected
        selected_category = qs.filter(date_created__gte=start_date)
        s_with_cat = qs.filter(date_created__gte=start_date).aggregate(baa=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('baa')
        

    if end_date != '' and end_date != None:
        qs = qs.filter(date_created__lt=end_date)
        count_with_data_selected = qs.filter(date_created__lt=end_date)

        # Suming amount based on only the end date selected
        selected_category = qs.filter(date_created__lt=end_date)
        s_with_cat = qs.filter(date_created__lt=end_date).aggregate(con=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('con')
    
    if expenses == 'on':
        qs = qs.filter(expenses=True)
        count_with_data_selected = qs.filter(expenses=True)
        
        # summing amount based on the expenses activated
        selected_category = qs.filter(expenses=True)
        s_with_cat = qs.filter(expenses=True).aggregate(ton=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('ton')

    elif not_expenses == 'on':
        qs = qs.filter(expenses=False)
        count_with_data_selected = qs.filter(expenses=False)

        
        # summing amount based on the expenses deactivated
        selected_category = qs.filter(expenses=False)
        s_with_cat = qs.filter(expenses=False).aggregate(tah=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('tah')  

    # getting the names from the form
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = request.GET.get('expenses')
    not_expenses = request.GET.get('not_expenses')

    
    if category != '' and category != None and category != 'Choose...':
        qs = qs.filter(category_id=category)
        count_with_data_selected = qs.filter(category_id=category)
        selected_category = get_object_or_404(WearCategory, id=category, category_owner_id=request.user.id)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table

        # Suming amount based on the category selected
        selected_category = get_object_or_404(WearCategory, id=category)
        s_with_cat = qs.filter(category_id=category).aggregate(ba=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('ba')

       
    
    if start_date != '' and start_date != None:
        qs = qs.filter(date_created__gte=start_date)
        count_with_data_selected = qs.filter(date_created__gte=start_date)

        # Suming amount based on only the start date selected
        selected_category = qs.filter(date_created__gte=start_date)
        s_with_cat = qs.filter(date_created__gte=start_date).aggregate(baa=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('baa')
        

    if end_date != '' and end_date != None:
        qs = qs.filter(date_created__lt=end_date)
        count_with_data_selected = qs.filter(date_created__lt=end_date)

        # Suming amount based on only the end date selected
        selected_category = qs.filter(date_created__lt=end_date)
        s_with_cat = qs.filter(date_created__lt=end_date).aggregate(con=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('con')
    
    if expenses == 'on':
        qs = qs.filter(expenses=True)
        count_with_data_selected = qs.filter(expenses=True)
        
        # summing amount based on the expenses activated
        selected_category = qs.filter(expenses=True)
        s_with_cat = qs.filter(expenses=True).aggregate(ton=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('ton')

    elif not_expenses == 'on':
        qs = qs.filter(expenses=False)
        count_with_data_selected = qs.filter(expenses=False)

        
        # summing amount based on the expenses deactivated
        selected_category = qs.filter(expenses=False)
        s_with_cat = qs.filter(expenses=False).aggregate(tah=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('tah')  

    form = CatSelectForm()
    queryset = Wear.objects.filter(activate=False)
    if request.method == 'POST':   
        form = CatSelectForm(request.POST or None)
        category = form['category'].value()
        
        
        if category != '':
            queryset = queryset.filter(category_id=category)
            count_with_category = queryset.filter(category_id=category)
            selected_category = get_object_or_404(WearCategory, id=category)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table
            s_with_cat = queryset.filter(category_id=category).aggregate(hu=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
            s_with_cat = s_with_cat.get('hu')

 
       
    wear_category = None  
    sum_wears_by_cat = None # I am declaring a variable here otherwise, this variable will not be recognize in the function

    categories = WearCategory.objects.filter(category_owner_id=request.user.id, activate=False)
    wears = Wear.objects.filter(user_id=request.user.id, activate=False)

    all_wears = Wear.objects.filter(user_id=request.user.id, activate=False).count()
    all_wears_cat = WearCategory.objects.filter(category_owner_id=request.user.id, activate=False)

    sum_all_wears = Wear.objects.filter(user_id=request.user.id, activate=False).aggregate(oga=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This is to sum all the wears
    sum_all_wears = sum_all_wears.get('oga') # This is to get the dict key and used this key to display everything
    
    deactivated_wearss = Wear.objects.filter(user_id=request.user.id, activate=False).count()
    deactivated_wears = Wear.objects.filter(user_id=request.user.id, activate=False)
    slice_deactivated_wears = Wear.objects.filter(user_id=request.user.id, activate=False)[:1]

   

    


  
    
    if wear_category_id:
        wear_category = get_object_or_404(WearCategory, id=wear_category_id, category_owner_id=request.user.id)
        wears = wears.filter(category=wear_category)
        sum_wears_by_cat = wears.filter(category=wear_category).aggregate(chai=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # sum wears based on the category filtered
        sum_wears_by_cat = sum_wears_by_cat.get('chai') # get the dict key so it's can be display on the template
    

    context = {
        'categories': categories,
        'wears': wears,
        'wear_category': wear_category,
        'sum_all_wears': sum_all_wears,
        'sum_wears_by_cat': sum_wears_by_cat,
        'all_wears': all_wears,
        'all_wears_cat': all_wears_cat,
        'form': form,
        'queryset': queryset,
        'count_with_category': count_with_category,
        'selected_category': selected_category,
        's_with_cat': s_with_cat,
        'deactivated_wears': deactivated_wears,
        'deactivated_wearss': deactivated_wearss,
        'slice_deactivated_wears': slice_deactivated_wears,
        'all_wear_categories': all_wear_categories,
        'qs': qs,
        's_with_cat': s_with_cat,
        'selected_category': selected_category,
        'count_with_data_selected': count_with_data_selected,
        'sum_all_d_wears': sum_all_d_wears,
        
           
    }
    
    return render(request, 'homapp/wears/deactivated_wears.html', context)



class WearDetailView(LoginRequiredMixin, DetailView):
    model = Wear
    template_name = 'homapp/wears/detail.html'



@login_required
def add_wear(request):  
    if request.method == 'POST':
        wear_register_form = WearRegisterForm(request.user, request.POST, request.FILES)
        if wear_register_form.is_valid():
            new_wear_reg = wear_register_form.save(commit=False)
            new_wear_reg.user_id = request.user.id
            new_wear_reg.save()
            messages.success(request, f'{ new_wear_reg.name } wear was added successfully'.title())
            return redirect('homapp:wears_list')
    else:
        wear_register_form = WearRegisterForm(request.user)

    context = {
        'new_wear_reg': wear_register_form,
        'wear_register_form': wear_register_form,
    }
    return render(request, 'homapp/wears/register_wear.html', context)


@login_required
def update_wear(request, wear_id):
    cati = WearCategory.objects.all().filter(activate=True).count()
    all_wears = Wear.objects.filter(activate=True).count()
    queryset = get_object_or_404(Wear, id=wear_id,)
    # queryset = Wear.objects.get(id=id) 
    form = WearEditForm(request.user, instance=queryset)
    if request.method == 'POST':
        form = WearEditForm(request.user, request.POST, request.FILES, instance=queryset)
        if form.is_valid():
            updated_wear = form.save(commit=False)
            updated_wear.user_id = request.user.id
            updated_wear.save()
            messages.success(request, f'{ updated_wear.name } was updated successfully by { request.user }'.title())
            return redirect('homapp:wears_list' +wear_id)
    context = {
        'updated_wear': queryset,   
        'form': form,
        'cati': cati,
        'all_wears': all_wears,
    }
    return render(request, 'homapp/wears/edit_wear.html', context)

@login_required
def delete_wear(request, id):
    get_id = get_object_or_404(Wear, id=id, user_id=request.user.id)
    if request.method == 'POST':
        get_id.delete()
        messages.success(request, f'{ get_id.name } wear was deleted successfully'.title())
        return redirect('homapp:wears_list')
    context = {
        'get_id': get_id,
    }
    return render(request, 'homapp/wears/delete_wear.html', context)






@login_required
def add_category(request):
    cati = WearCategory.objects.all().filter(category_owner_id=request.user.id,activate=True).count()
    all_wears = Wear.objects.filter(user_id=request.user.id, activate=True).count()
    if request.method == 'POST':
        cat_add_form = AddCategoryForm(request.POST)
        if cat_add_form.is_valid():
            new_cat = cat_add_form.save(commit=False)
            new_cat.category_owner_id = request.user.id  
            new_cat.save()
            messages.success(request, f'{ new_cat.category_name } was added successfully'.title())
            return redirect('homapp:category_list')
    else:
        cat_add_form = AddCategoryForm()
    context = {
        'cat_add_form': cat_add_form,
        'new_cat': cat_add_form,
        'cati': cati,
        'all_wears': all_wears,
    }
    return render(request, 'homapp/wears/add_category.html', context)


@login_required
def category_list(request):
    categories = WearCategory.objects.filter(category_owner_id=request.user.id, activate=True)
    cati = WearCategory.objects.all().filter(category_owner_id=request.user.id, activate=True).count()
    all_wears = Wear.objects.filter(user_id=request.user.id, activate=True).count()
    last_add_category = WearCategory.objects.filter(category_owner_id=request.user.id, activate=True)[:1]
    deactivated_category = WearCategory.objects.filter(category_owner_id=request.user.id, activate=False).count()
    context = {
        'categories': categories,
        'cati': cati,
        'all_wears': all_wears,
        'last_add_category': last_add_category,
        'deactivated_category': deactivated_category,

    }
    return render(request, 'homapp/wears/category_list.html', context)


@login_required
def deactivated_category(request):
    all_deactivated_categories = WearCategory.objects.filter(category_owner_id=request.user.id, activate=False).count()
    all_activated_categories = WearCategory.objects.filter(category_owner_id=request.user.id, activate=True).count()
    all_deact_categories = WearCategory.objects.filter(category_owner_id=request.user.id, activate=False)
    last_added_category = WearCategory.objects.filter(category_owner_id=request.user.id, activate=True)[:1]
    total_wears = Wear.objects.filter(user_id=request.user.id, activate=True).count()

    context = {
        'all_deactivated_categories': all_deactivated_categories,
        'all_deact_categories': all_deact_categories,
        'all_activated_categories': all_activated_categories,
        'last_added_category': last_added_category,
        'total_wears': total_wears,
    }
    return render(request, 'homapp/wears/deactivated_category.html', context)


@login_required
def edit_category(request, pk):
    cati = WearCategory.objects.all().filter(category_owner_id=request.user.id, activate=True).count()
    all_wears = Wear.objects.filter(user_id=request.user.id, activate=True).count()
    queryset = get_object_or_404(WearCategory, id=pk, category_owner_id=request.user.id)
    cat_edit_form = CatEditForm(instance=queryset)
    if request.method == 'POST':
        cat_edit_form = CatEditForm(request.POST, instance=queryset)
        if cat_edit_form.is_valid():
            new_category = cat_edit_form.save(commit=False)
            new_category.category_owner_id = request.user.id
            new_category.save()
            messages.success(request, f'{ new_category.category_name } was successfully updated'.title())
            return redirect('homapp:category_list')
    context = {
        'cat_edit_form': cat_edit_form,
        'new_category': queryset,
        'cati': cati, 
        'all_wears': all_wears,
    }
    return render(request, 'homapp/wears/edit_category.html', context)

@login_required
def delete_category(request, pk):
    queryset = get_object_or_404(WearCategory, id=pk, category_owner_id=request.user.id)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, f'{queryset.category_name} was deleted successfully'.title())
        return redirect('homapp:category_list')
    context = {
        'queryset': queryset,
    }
    return render(request, 'homapp/wears/delete_category.html', context)

            
    

# @login_required
# def clothe_list(request, category_slug=None):
#     category = None  
#     sum_clothe_by_cat = None
#     categories = ClotheCategory.objects.all()
#     clothes = Clothe.objects.all()
    # sum_clothes = Clothe.objects.all().aggregate(hod=Sum('clothe_amount')) # This is to sum all the clothes
    # sum_clothes = sum_clothes.get('hod') # This is to get the key for the value of the clothes sum and the key here is 'clothe_amount__sum'
    # if category_slug:
    #     category = get_object_or_404(ClotheCategory, slug=category_slug)
    #     clothes = clothes.filter(category=category)
        # sum_clothe_by_cat = clothes.filter(category=category).aggregate(Sum('clothe_amount')) # This is to sum all the clothes by category
        # sum_clothe_by_cat = sum_clothe_by_cat.get('clothe_amount__sum')           # This is to get the key for the value of the clothes sum by category and the key here is 'clothe_amount__sum'
    # return render(request, 'homapp/clothes/list.html', {'categories': categories,
    #                                                     'category': category,
    #                                                     'clothes': clothes,
    #                                                     'sum_clothes': sum_clothes,
    #                                                     'sum_clothe_by_cat': sum_clothe_by_cat })

# @login_required
# def wear_detail(request, pk):
#     single_wear = get_object_or_404(Wear, id=pk, activate=True)
#     context = {'single_wear': single_wear,}

#     return render(request, 'homapp/wears/details.html', context)

# @login_required
# def clothe_detail(request,  year, month, day, id, slug,):
#     clothe = get_object_or_404(Clothe, slug=slug,
#                                        activate__year=year,
#                                        activate__month=month,
#                                        activate__day=day,
#                                        id=id,
                                       
#                                        )
#     return render(request, 'homapp/clothes/detail.html', {'clothe': clothe })
@login_required
def finance_list(request):
    count_with_category = None
    selected_category = None
    s_with_cat = None
    sum_all_finances = None

    s_with_cat = None 
    selected_category = None
    count_finance_data_selected = None

    finances = Finance.objects.filter(user_id=request.user.id, activate=True)
    all_fin_categories = FinanceCategory.objects.filter(activate=True, category_owner_id=request.user.id)
    last_added_finance = Finance.objects.filter(activate=True, user_id=request.user.id)[:1] # To show the last added objects and slice the result to be one showing...
    deactivate_finances_count = Finance.objects.filter(activate=False, user_id=request.user.id).count()

    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = request.GET.get('expenses')
    not_expenses = request.GET.get('not_expenses')
    search = request.GET.get('search')


    if category != '' and category != None and category != 'Choose...':
        finances = finances.filter(category_id=category)
        count_finance_data_selected = finances.filter(category_id=category)
        selected_category = get_object_or_404(FinanceCategory, id=category)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table

        # Suming amount based on the category selected
        selected_category = get_object_or_404(FinanceCategory, id=category)
        s_with_cat = finances.filter(category_id=category).aggregate(ba=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('ba')

       
    
    if start_date != '' and start_date != None:
        finances = finances.filter(date_created__gte=start_date)
        count_finance_data_selected = finances.filter(date_created__gte=start_date)

        # Suming amount based on only the start date selected
        selected_category = finances.filter(date_created__gte=start_date)
        s_with_cat = finances.filter(date_created__gte=start_date).aggregate(baa=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('baa')
        

    if end_date != '' and end_date != None:
        finances = finances.filter(date_created__lt=end_date)
        count_finance_data_selected = finances.filter(date_created__lt=end_date)

        # Suming amount based on only the end date selected
        selected_category = finances.filter(date_created__lt=end_date)
        s_with_cat = finances.filter(date_created__lt=end_date).aggregate(con=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('con')


    if search != '' and search != None: 
        finances = finances.filter(title__icontains=search)
        count_finance_data_selected = finances.filter(title__icontains=search)

        # summing amount based on the word search on
        selected_category = finances.filter(title__icontains=search)
        s_with_cat = finances.filter(title__icontains=search).aggregate(hjo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('hjo')
    

    
    if expenses == 'on':
        finances = finances.filter(expenses=True)
        count_finance_data_selected = finances.filter(expenses=True)
        
        # summing amount based on the expenses activated
        selected_category = finances.filter(expenses=True)
        s_with_cat = finances.filter(expenses=True).aggregate(ton=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('ton')

    elif not_expenses == 'on':
        finances = finances.filter(expenses=False)
        count_finance_data_selected = finances.filter(expenses=False)

        
        # summing amount based on the expenses activated
        selected_category = finances.filter(expenses=False)
        s_with_cat = finances.filter(expenses=False).aggregate(tah=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('tah')


    form = FinCatSelectForm(request.user)
    if request.method == 'POST':
        form = FinCatSelectForm(request.user, request.POST or None)
        category = form['category'].value()

        if category != '':
            finances = finances.filter(category_id=category)
            count_with_category = finances.filter(category_id=category) # This will count the category based on what is passed in..
            selected_category = get_object_or_404(FinanceCategory, id=category)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table

            s_with_cat = finances.filter(category_id=category).aggregate(hu=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
            s_with_cat = s_with_cat.get('hu')

    sum_all_finances = Finance.objects.filter(user_id=request.user.id, activate=True).aggregate(oga=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This is to sum all the Finance
    sum_all_finances = sum_all_finances.get('oga') # This is to get the dict key and used this key to display everything


    context = {
        'finances': finances,
        'all_fin_categories':all_fin_categories,
        'form': form,
        'count_finance_data_selected': count_finance_data_selected,
        'selected_category': selected_category,
        's_with_cat':  s_with_cat,
        'sum_all_finances': sum_all_finances,
        'last_added_finance': last_added_finance,
        'deactivate_finances_count': deactivate_finances_count,

            
    }
    return render(request, 'homapp/finance/finance_list.html', context)

class FinanceDetailView(LoginRequiredMixin, DetailView):
    model = Finance
    template_name = 'homapp/finance/finance_detail.html'

@login_required
def add_finance(request):
    if request.method == 'POST':
        finance_add_form = FinanceAddForm(request.user, request.POST, request.FILES)
        if finance_add_form.is_valid():
            new_finance = finance_add_form.save(commit=False)
            new_finance.user_id = request.user.id   
            new_finance.save()
            messages.success(request, f'{new_finance.title} was added successfully'.title())
            return redirect('homapp:all_transactions')
    else:
        finance_add_form = FinanceAddForm(request.user)
    context = {
        'new_finance': finance_add_form,
        'finance_add_form': finance_add_form,
    }
    return render(request, 'homapp/finance/add_finance.html', context)

@login_required
def edit_finance(request, pk):
    queryset = get_object_or_404(Finance, id=pk)
    finance_edit_form = EditFinanceForm(request.user, instance=queryset)
    if request.method == 'POST':
        finance_edit_form = EditFinanceForm(request.user, request.POST, request.FILES, instance=queryset)
        if finance_edit_form.is_valid():
            new_form = finance_edit_form.save(commit=False)
            new_form.user_id = request.user.id   
            new_form.save()
            messages.success(request, f'{new_form.title} was updated successfully'.title())
            return redirect('homapp:all_transactions')
    context = {
        'new_form': queryset,
        'finance_edit_form': finance_edit_form,
    }
    return render(request, 'homapp/finance/edit_finance.html', context)

@login_required
def delete_finance(request, pk):
    queryset = get_object_or_404(Finance, id=pk, user_id=request.user.id)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, f'{queryset.title} was deleted successfully'.title())
        return redirect('homapp:all_transactions')
    context = {
        'queryset': queryset,
    }
    return render(request, 'homapp/finance/delete_finance.html', context)

@login_required
def finance_cat_list(request):
    all_fin_categories = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=True)
    finances = Finance.objects.filter(user_id=request.user.id, activate=True)
    all_fin_cat = FinanceCategory.objects.filter(category_owner_id=request.user.id,activate=True).count()
    last_added_fin_category = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=True)[:1]
    all_deactivated_category = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=False).count()

    context = {
        'all_fin_categories': all_fin_categories,
        'finances': finances,
        'all_fin_cat': all_fin_cat,
        'last_added_fin_category': last_added_fin_category,
        'all_deactivated_category': all_deactivated_category,
    }
    return render(request, 'homapp/finance/finance_cat_list.html', context)

@login_required
def add_fin_category(request):
    if request.method == 'POST':
        add_fin_category_form = AddFinanceCategoryForm(request.POST)
        if add_fin_category_form.is_valid():
            new_fin_cat = add_fin_category_form.save(commit=False)
            new_fin_cat.category_owner_id = request.user.id   
            new_fin_cat.save()
            messages.success(request, f'{new_fin_cat.category_name} was added successfully'.title())
            return redirect('homapp:finance_cat_list')
    else:
        add_fin_category_form = AddFinanceCategoryForm()
    context = {
        'new_fin_cat': add_fin_category_form, 
        'add_fin_category_form': add_fin_category_form,
    }
    return render(request, 'homapp/finance/add_fin_category.html', context)

@login_required
def edit_fin_category(request, pk):
    queryset = get_object_or_404(FinanceCategory, id=pk)
    edit_fin_form = FinanceCatEditForm(instance=queryset)
    if request.method == 'POST':
        edit_fin_form = FinanceCatEditForm(request.POST, instance=queryset)
        if edit_fin_form.is_valid():
            new_edit = edit_fin_form.save(commit=False)
            new_edit.category_owner_id = request.user.id  
            new_edit.save()
            messages.success(request, f'{new_edit.category_name} was updated successfully'.title())
            return redirect('homapp:finance_cat_list')
    context = {
        'new_edit': queryset, 
        'edit_fin_form': edit_fin_form,
    }
    return render(request, 'homapp/finance/edit_fin_category.html', context)

@login_required
def delete_fin_category(request, pk):
    queryset = get_object_or_404(FinanceCategory, id=pk, category_owner_id=request.user.id)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, f'{queryset.category_name} was deleted successfully'.title())
        return redirect('homapp:finance_cat_list')
    context = {
        'queryset': queryset,
    }
    return render(request, 'homapp/finance/delete_fin_category.html', context)



@login_required
def deactivated_finances(request):
    count_with_category = None
    selected_category = None
    s_with_cat = None
    sum_all_finances = None
    count_finance_data_selected = None
    sum_all_dect_amount = None
    

    

    all_deactivated_finances = Finance.objects.filter(user_id=request.user.id, activate=False)

    # Am summing all deactivated finance amount
    sum_all_dect_finances = Finance.objects.filter(user_id=request.user.id, activate=False).aggregate(zy=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This is to sum all the Finance
    sum_all_dect_finances = sum_all_dect_finances.get('zy') # This is to get the dict key and used this key to display everything



    # last added finance
    last_added_finance = Finance.objects.filter(user_id=request.user.id, activate=True)[:1]
    
    # last deactivated finance
    last_deactivated_finance = Finance.objects.filter(user_id=request.user.id, activate=False)[:1] # To show the last added objects and slice the result to be one showing...
    
    deactivate_finances_count = Finance.objects.filter(user_id=request.user.id, activate=False).count()
    # all total number of finance
    total_n_finance = Finance.objects.filter(user_id=request.user.id, activate=True).count()

    # All finance categories
    all_fin_categories = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=True)

    
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = request.GET.get('expenses')
    not_expenses = request.GET.get('not_expenses')
    search = request.GET.get('search')

    if category != '' and category != None and category != 'Choose...':
        all_deactivated_finances = all_deactivated_finances.filter(user_id=request.user.id, category_id=category)
        count_finance_data_selected = all_deactivated_finances.filter(user_id=request.user.id, category_id=category)
        selected_category = get_object_or_404(FinanceCategory, id=category)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table

        # Suming amount based on the category selected
        selected_category = get_object_or_404(FinanceCategory, id=category)
        s_with_cat = all_deactivated_finances.filter(user_id=request.user.id,category_id=category).aggregate(ba=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('ba')

       
    
    if start_date != '' and start_date != None:
        all_deactivated_finances = all_deactivated_finances.filter(user_id=request.user.id, date_created__gte=start_date)
        count_finance_data_selected = all_deactivated_finances.filter(user_id=request.user.id, date_created__gte=start_date)

        # Suming amount based on only the start date selected
        selected_category = all_deactivated_finances.filter(user_id=request.user.id, date_created__gte=start_date)
        s_with_cat = all_deactivated_finances.filter(user_id=request.user.id, date_created__gte=start_date).aggregate(baa=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('baa')
        

    if end_date != '' and end_date != None:
        all_deactivated_finances = all_deactivated_finances.filter(user_id=request.user.id, date_created__lt=end_date)
        count_finance_data_selected = all_deactivated_finances.filter(user_id=request.user.id, date_created__lt=end_date)

        # Suming amount based on only the end date selected
        selected_category = all_deactivated_finances.filter(user_id=request.user.id, date_created__lt=end_date)
        s_with_cat = all_deactivated_finances.filter(user_id=request.user.id, date_created__lt=end_date).aggregate(con=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('con')


    
    if search != '' and search != None: 
        all_deactivated_finances = all_deactivated_finances.filter(user_id=request.user.id, title__icontains=search)
        count_finance_data_selected = all_deactivated_finances.filter(user_id=request.user.id, title__icontains=search)

        # summing amount based on the word search on
        selected_category = all_deactivated_finances.filter(user_id=request.user.id, title__icontains=search)
        s_with_cat = all_deactivated_finances.filter(user_id=request.user.id, title__icontains=search).aggregate(ho=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('ho')
    


    if expenses == 'on':
        all_deactivated_finances = all_deactivated_finances.filter(user_id=request.user.id,expenses=True)
        count_finance_data_selected =all_deactivated_finances.filter(user_id=request.user.id,expenses=True)
        
        # summing amount based on the expenses activated
        selected_category = all_deactivated_finances.filter(user_id=request.user.id,expenses=True)
        s_with_cat = all_deactivated_finances.filter(user_id=request.user.id,expenses=True).aggregate(ton=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('ton')

    elif not_expenses == 'on':
        all_deactivated_finances = all_deactivated_finances.filter(user_id=request.user.id,expenses=False)
        count_finance_data_selected = all_deactivated_finances.filter(user_id=request.user.id,expenses=False)

        
        # summing amount based on the expenses activated
        selected_category = all_deactivated_finances.filter(user_id=request.user.id, expenses=False)
        s_with_cat = all_deactivated_finances.filter(user_id=request.user.id, expenses=False).aggregate(tah=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('tah')


    context = {
        'count_with_category': count_with_category,
        'selected_category': selected_category,
        's_with_cat':  s_with_cat,
        'sum_all_finances': sum_all_finances,
        'last_deactivated_finance': last_deactivated_finance,
        'deactivate_finances_count': deactivate_finances_count,
        'all_deactivated_finances': all_deactivated_finances,
        'total_n_finance': total_n_finance,
        'last_added_finance': last_added_finance,
        'count_finance_data_selected': count_finance_data_selected,
        'all_fin_categories': all_fin_categories,
        'sum_all_dect_amount': sum_all_dect_amount,
        'sum_all_dect_finances': sum_all_dect_finances,

            
    }
    return render(request, 'homapp/finance/all_deactivated_finances.html', context)


# for editing finance deactivated page
@login_required
def edit_finance_deactivated(request, pk):
    queryset = get_object_or_404(Finance, id=pk)
    finance_deactivated_edit_form = EditFinanceDectForm(request.user, instance=queryset)
    if request.method == 'POST':
        finance_deactivated_edit_form = EditFinanceDectForm(request.user, request.POST, instance=queryset)
        if finance_deactivated_edit_form.is_valid():
            new_form = finance_deactivated_edit_form.save(commit=False)
            new_form.user_id = request.user.id   
            new_form.save()
            messages.success(request, f'{new_form.title} was updated successfully'.title())
            return redirect('homapp:deactivated_finances')
    context = {
        'new_form': queryset,
        'finance_deactivated_edit_form': finance_deactivated_edit_form,
    }
    return render(request, 'homapp/finance/edit_finance_deactivated.html', context)




# for finance deactivated delete page
@login_required
def delete_deactivated_finance(request, pk):
    qs = get_object_or_404(Finance, id=pk, user_id=request.user.id)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f'{qs.title} was deleted successfully'.title())
        return redirect('homapp:deactivated_finances')
    context = {
        'qs': qs,
    }
    return render(request, 'homapp/finance/delete_deactivated_finance.html', context)




# For all deactivated finance categories..
@login_required
def deactivated_finance_category(request):
    all_deactivated_finance_categories = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=False).count()
    all_activated_finance_categories = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=True).count()
    all_deact_finance_categories = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=False)
    last_added_finance_category = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=False)[:1]
    total_finance = Finance.objects.filter(user_id=request.user.id, activate=True).count()

    context = {
        'all_deactivated_finance_categories': all_deactivated_finance_categories,
        'all_activated_finance_categories': all_activated_finance_categories,
        'all_deact_finance_categories': all_deact_finance_categories,
        'last_added_finance_category': last_added_finance_category,
        'total_finance': total_finance,
    }
    return render(request, 'homapp/finance/deactivated_finance_category.html', context)




# Edit finance deactivated categories page
@login_required
def finance_deactivated_edit_category(request, pk):
    new_fin_dect = None
    # Total finance category
    total_finance_categories = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=True).count()

    # last added finance category
    last_added_finance_category = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=True)[:1]

    # last deactivated finance category
    last_deactivated_category = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=False)[:1]

    finance_deactivated_cat = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=False).count()
    queryset = get_object_or_404(FinanceCategory, category_owner_id=request.user.id, activate=False, id=pk)
    finance_deactivated_category_form = FinanceDeactivatedCatForm(instance=queryset)
    if request.method == 'POST':
        finance_deactivated_category_form = FinanceDeactivatedCatForm(request.POST, instance=queryset)
        if finance_deactivated_category_form.is_valid():
            new_fin_dect = finance_deactivated_category_form.save(commit=False)
            new_fin_dect.category_owner_id = request.user.id
            new_fin_dect.save()
            messages.success(request, f'{ new_fin_dect.category_name } was successfully updated'.title())
            return redirect('homapp:deactivated_finance_category')

    context = {
        'finance_deactivated_category_form': finance_deactivated_category_form,
        'new_fin_dect': new_fin_dect,
        'finance_deactivated_cat': finance_deactivated_cat,
        'total_finance_categories': total_finance_categories,
        'last_added_finance_category': last_added_finance_category,
        'last_deactivated_category': last_deactivated_category,
    }
    return render(request, 'homapp/finance/finance_deactivated_edit_category.html', context)



# delete finance deactivated category
@login_required
def delete_fin_deactivated_category(request, pk):
    queryset = get_object_or_404(FinanceCategory, id=pk, category_owner_id=request.user.id)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, f'{queryset.category_name} was deleted successfully'.title())
        return redirect('homapp:deactivated_finance_category')
    context = {
        'queryset': queryset,
    }
    return render(request, 'homapp/finance/delete_fin_deactivated_category.html', context)





@login_required
def all_transactions(request):
    count_with_category = None
    selected_category = None
    s_with_cat = None
    count_finance_data_selected = None

    finances = Finance.objects.filter(user_id=request.user.id, activate=True)
    c_expenses = Finance.objects.filter(user_id=request.user.id, expenses=True).count()
    c_income = Finance.objects.filter(user_id=request.user.id, expenses=False).count()
    all_fin_categories = FinanceCategory.objects.filter(category_owner_id=request.user.id, activate=True)


    sum_expenses = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True).aggregate(x=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    sum_expenses = sum_expenses.get('x')

    sum_income = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False).aggregate(y=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    sum_income = sum_income.get('y')

    sum_all_finances = Finance.objects.filter(user_id=request.user.id, activate=True).aggregate(z=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This is to sum all the Finance
    sum_all_finances = sum_all_finances.get('z') # This is to get the dict key and used this key to display everything




    
    form = FinCatSelectForm(request.user)

    if request.method == 'POST':
        form = FinCatSelectForm(request.user, request.POST or None)
        category = form['category'].value()
    
    # for pagination
    # paginator = Paginator(finances, 1)
    # page = request.GET.get('page', 1)

    # try:
    #     finances = paginator.page(page)
    # except PageNotAnInteger:
    #     finances = paginator.page(1)
    # except EmptyPage:
    #     finances = paginator.page(paginator.num_pages)
        

    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = request.GET.get('expenses')
    not_expenses = request.GET.get('not_expenses')
    search = request.GET.get('search')

    if category != '' and category != None and category != 'Choose...':
        finances = finances.filter(user_id=request.user.id, category_id=category)
        count_finance_data_selected = finances.filter(user_id=request.user.id, category_id=category)
        selected_category = get_object_or_404(FinanceCategory, id=category)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table

        # Suming amount based on the category selected
        selected_category = get_object_or_404(FinanceCategory, id=category)
        s_with_cat = finances.filter(user_id=request.user.id,category_id=category).aggregate(ba=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('ba')

       
    
    if start_date != '' and start_date != None:
        finances = finances.filter(user_id=request.user.id, date_created__gte=start_date)
        count_finance_data_selected = finances.filter(user_id=request.user.id, date_created__gte=start_date)

        # Suming amount based on only the start date selected
        selected_category = finances.filter(user_id=request.user.id, date_created__gte=start_date)
        s_with_cat = finances.filter(user_id=request.user.id, date_created__gte=start_date).aggregate(baa=Coalesce(Sum('amount'), V(0), output_field=DecimalField())) # This will sum based on the category selected
        s_with_cat = s_with_cat.get('baa')
        

    if end_date != '' and end_date != None:
        finances = finances.filter(user_id=request.user.id, date_created__lt=end_date)
        count_finance_data_selected = finances.filter(user_id=request.user.id, date_created__lt=end_date)

        # Suming amount based on only the end date selected
        selected_category = finances.filter(user_id=request.user.id, date_created__lt=end_date)
        s_with_cat = finances.filter(user_id=request.user.id, date_created__lt=end_date).aggregate(con=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('con')


    
    if search != '' and search != None: 
        finances = finances.filter(Q(title__icontains=search) | Q(amount__icontains=search), user_id=request.user.id)
        count_finance_data_selected = finances.filter(Q(title__icontains=search) | Q(amount__icontains=search), user_id=request.user.id)

        # summing amount based on the word search on
        selected_category = finances.filter(Q(title__icontains=search) | Q(amount__icontains=search), user_id=request.user.id)
        s_with_cat = finances.filter(user_id=request.user.id, title__icontains=search).aggregate(ho=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('ho')
    


    if expenses == 'on':
        finances = finances.filter(user_id=request.user.id,expenses=True)
        count_finance_data_selected = finances.filter(user_id=request.user.id,expenses=True)
        
        # summing amount based on the expenses activated
        selected_category = finances.filter(user_id=request.user.id,expenses=True)
        s_with_cat = finances.filter(user_id=request.user.id,expenses=True).aggregate(ton=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('ton')

    elif not_expenses == 'on':
        finances = finances.filter(user_id=request.user.id,expenses=False)
        count_finance_data_selected = finances.filter(user_id=request.user.id,expenses=False)

        
        # summing amount based on the expenses activated
        selected_category = finances.filter(user_id=request.user.id, expenses=False)
        s_with_cat = finances.filter(user_id=request.user.id, expenses=False).aggregate(tah=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
        s_with_cat = s_with_cat.get('tah')



    context = {
        'finances': finances,
        'form': form,
        'count_with_category': count_with_category,
        'selected_category': selected_category,
        's_with_cat': s_with_cat,
        'c_expenses': c_expenses,
        'c_income': c_income,
        'sum_expenses': sum_expenses,
        'sum_income': sum_income,
        'sum_all_finances': sum_all_finances,
        'count_finance_data_selected': count_finance_data_selected,
        'all_fin_categories': all_fin_categories,
       
    }
    return render(request, 'homapp/finance/all_transactions.html', context)



    # I sum the total amount in wear table......
    wear_total_amount = Wear.objects.aggregate(g=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    wear_total_amount = wear_total_amount.get('g')


    # I sum the total amount in finance table here......
    finance_total_amount = Finance.objects.aggregate(w=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    finance_total_amount = finance_total_amount.get('w')

    # I now add two of them together to obtain the grand total...
    adding_everything = wear_total_amount + finance_total_amount





    # I sum the total income in wear table
    wear_income = Wear.objects.filter(expenses=False).aggregate(xo=Coalesce(Sum('amount'), V(0)))
    wear_income = wear_income.get('xo')

    # I sum the total income in finance table
    finance_income = Finance.objects.filter(expenses=False).aggregate(yo=Coalesce(Sum('amount'), V(0)))
    finance_income = finance_income.get('yo')

    # I then total the two of them to get the grand total
    grand_income = wear_income + finance_income





    # I sum the total expenses in wear table
    wear_expenses = Wear.objects.filter(expenses=True).aggregate(xo=Coalesce(Sum('amount'), V(0)))
    wear_expenses = wear_expenses.get('xo')

    # I sum the total expenses in finance table

    finance_expenses = Finance.objects.filter(expenses=True).aggregate(yo=Coalesce(Sum('amount'), V(0)))
    finance_expenses = finance_expenses.get('yo')

    
    # I then add two of them together to get the grand expenses amount
    grand_expenses = wear_expenses + finance_expenses
    
    
   


    context = {
        'adding_everything': adding_everything,
        'grand_income': grand_income,
        'grand_expenses': grand_expenses,
        'wear_income': wear_income, 
        'finance_income': finance_income,
        'wear_expenses': wear_expenses,
        'finance_expenses': finance_expenses,
    }
    return render(request, 'homapp/finance/account_summary.html', context)


@login_required
def today_summary(request):
    today_date = date.today()

    count_today_wear_income = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__date=today_date).count()
    count_today_finance_income = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__date=today_date).count()
    all_today_income_count = count_today_wear_income + count_today_finance_income


    count_today_wear_expenses = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__date=today_date).count()
    count_today_finance_expenses = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__date=today_date).count()
    all_today_expenses_count = count_today_wear_expenses + count_today_finance_expenses


    counting_today_wear_data = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__date=today_date).count()
    counting_today_finance_data = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__date=today_date).count()
    all_data_for_today = counting_today_wear_data + counting_today_finance_data

    # getting wear total income for today alone
    wear_total_income_amount_for_today = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__date=today_date).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    wear_total_income_amount_for_today = wear_total_income_amount_for_today.get('xo')
    
    # getting finance total income for today alone 
    finance_total_income_amount_for_today = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__date=today_date).aggregate(yo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    finance_total_income_amount_for_today = finance_total_income_amount_for_today.get('yo')

    today_total_income = wear_total_income_amount_for_today + finance_total_income_amount_for_today


    # getting wear total expenses for today alone
    wear_total_expenses_amount_for_today = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__date=today_date).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    wear_total_expenses_amount_for_today = wear_total_expenses_amount_for_today.get('xo')

    # getting finance total expenses for today alone 
    finance_total_expenses_amount_for_today = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__date=today_date).aggregate(yo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    finance_total_expenses_amount_for_today = finance_total_expenses_amount_for_today.get('yo')

    today_total_expenses = wear_total_expenses_amount_for_today + finance_total_expenses_amount_for_today


    all_amount_for_today = today_total_income + today_total_expenses

    # Today wear total amount
    today_wear_total_amount = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__date=today_date).aggregate(ty=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    today_wear_total_amount = today_wear_total_amount.get('ty')

    # Today Finance total amount
    today_finance_total_amount = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__date=today_date).aggregate(tp=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    today_finance_total_amount = today_finance_total_amount.get('tp')
    
    

    context = {
        'today_date': today_date,
        # for income
        'wear_total_income_amount_for_today': wear_total_income_amount_for_today,
        'finance_total_income_amount_for_today': finance_total_income_amount_for_today,
        'today_total_income': today_total_income,

        # for expenses
        'wear_total_expenses_amount_for_today': wear_total_expenses_amount_for_today,
        'finance_total_expenses_amount_for_today': finance_total_expenses_amount_for_today,
        'today_total_expenses': today_total_expenses,

        'all_amount_for_today': all_amount_for_today,
        'all_data_for_today': all_data_for_today,

        'all_today_income_count': all_today_income_count,
        'all_today_expenses_count': all_today_expenses_count,

        'count_today_wear_income': count_today_wear_income,
        'count_today_finance_income': count_today_finance_income,

        'count_today_wear_expenses': count_today_wear_expenses,
        'count_today_finance_expenses': count_today_finance_expenses,

        'counting_today_wear_data': counting_today_wear_data,
        'counting_today_finance_data': counting_today_finance_data,

        # today_wear_total_amount
        'today_wear_total_amount': today_wear_total_amount,
        'today_finance_total_amount': today_finance_total_amount,


    }
    return render(request, 'homapp/finance/today_summary.html', context)




# last 3 days summary  
@login_required
def last_3_days(request):
    
    today = timezone.now()
    last_3_days = today - timedelta(days=3)

    # counting last 3 days wear income alone
    last_3_days_wear_income_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__range=(last_3_days, today)).count()

     # counting last 3 days wear income alone
    last_3_days_finance_income_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__range=(last_3_days, today)).count()

    # summing up last 3 days income from both wears and finance together
    income_for_last_3_days = last_3_days_wear_income_count + last_3_days_finance_income_count



    # counting last 3 days wear expenses alone  
    last_3_days_wear_expenses_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__range=(last_3_days, today)).count()

    # counting last 3 days finance expenses alone
    last_3_days_finance_expenses_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__range=(last_3_days, today)).count()

    # summing up last 3 days expenses from both wears and finance together
    expenses_for_last_3_days = last_3_days_wear_expenses_count + last_3_days_finance_expenses_count



    last_3_days_wear_count = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_3_days, today)).count()
    last_3_days_finance_count = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_3_days, today)).count()

    # summing total data for last 3 days  
    last_3_days_data_count = last_3_days_wear_count + last_3_days_finance_count  

    # Last 3 days wear income
    last_3_days_wear_income = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__range=(last_3_days, today)).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_3_days_wear_income = last_3_days_wear_income.get('xo')

    # Last 3 days Finance income
    last_3_days_finance_income = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__range=(last_3_days, today)).aggregate(yo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_3_days_finance_income = last_3_days_finance_income.get('yo')

    # sum all last_3_days income together  last_3_days_finance_count
    sum_last_3_days_income = last_3_days_wear_income + last_3_days_finance_income


    # last 3 days wear expenses
    last_3_days_wear_expenses = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__range=(last_3_days, today)).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_3_days_wear_expenses = last_3_days_wear_expenses.get('xo')

    # last 3 days finance expenses
    last_3_days_finance_expenses = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__range=(last_3_days, today)).aggregate(uo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_3_days_finance_expenses = last_3_days_finance_expenses.get('uo')

    # sum all last_3_days expenses together  
    sum_last_3_days_expenses = last_3_days_wear_expenses + last_3_days_finance_expenses


    # summing amount for last 3 days
    total_amount_for_last_3_days = sum_last_3_days_income + sum_last_3_days_expenses

    # last 3 days wear total Amount 
    last_3_days_wear_total_amount = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_3_days, today)).aggregate(ro=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_3_days_wear_total_amount = last_3_days_wear_total_amount.get('ro')

    # last 3 days finance total Amount 
    last_3_days_finance_total_amount = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_3_days, today)).aggregate(ra=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_3_days_finance_total_amount = last_3_days_finance_total_amount.get('ra')




    context = {
        # counting last 3 days income data for both wears and finance and summing them together
        'last_3_days_wear_income_count': last_3_days_wear_income_count,
        'last_3_days_finance_income_count': last_3_days_finance_income_count,
        'income_for_last_3_days': income_for_last_3_days,

        # counting last 3 days expenses data for both wears and finance and summing them together
        'last_3_days_wear_expenses_count': last_3_days_wear_expenses_count,
        'last_3_days_finance_expenses_count': last_3_days_finance_expenses_count,
        'expenses_for_last_3_days': expenses_for_last_3_days,


        # last 3 days data count
        'last_3_days_wear_count': last_3_days_wear_count,    # counting all wear for the last 3 days
        'last_3_days_finance_count': last_3_days_finance_count, # counting all finance for the last 3 days
        'last_3_days_data_count': last_3_days_data_count,    # summing all of the to get the total data for the last 3 days

        # last 3 days income for both wear and finance
        'last_3_days_wear_income': last_3_days_wear_income,
        'last_3_days_finance_income': last_3_days_finance_income,
        'sum_last_3_days_income': sum_last_3_days_income,

        # last 3 days expenses for both wear and finance
        'last_3_days_wear_expenses': last_3_days_wear_expenses,
        'last_3_days_finance_expenses': last_3_days_finance_expenses,
        'sum_last_3_days_expenses': sum_last_3_days_expenses,

        # total amount for last 3 days
        'total_amount_for_last_3_days': total_amount_for_last_3_days,


        # last_3_days_wear_total_amount
        'last_3_days_wear_total_amount': last_3_days_wear_total_amount,

        # last_3_days_finance_total_amount
        'last_3_days_finance_total_amount': last_3_days_finance_total_amount,


    }
    return render(request, 'homapp/finance/last_3_days.html', context)


# last 7 days summary  

@login_required
def last_7_days(request):
    
    today = timezone.now()
    last_7_days = today - timedelta(days=7)

    # counting last 7 days wear income alone
    last_7_days_wear_income_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__range=(last_7_days, today)).count()

     # counting last 7 days wear income alone
    last_7_days_finance_income_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__range=(last_7_days, today)).count()

    # summing up last 7 days income from both wears and finance together
    income_for_last_7_days = last_7_days_wear_income_count + last_7_days_finance_income_count



    # counting last 7 days wear expenses alone  
    last_7_days_wear_expenses_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__range=(last_7_days, today)).count()

    # counting last 7 days finance expenses alone
    last_7_days_finance_expenses_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__range=(last_7_days, today)).count()

    # summing up last 7 days expenses from both wears and finance together
    expenses_for_last_7_days = last_7_days_wear_expenses_count + last_7_days_finance_expenses_count


    last_7_days_wear_count = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_7_days, today)).count()
    last_7_days_finance_count = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_7_days, today)).count()

    # summing total data for last 7 days  
    last_7_days_data_count = last_7_days_wear_count + last_7_days_finance_count  

    # Last 7 days wear income
    last_7_days_wear_income = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__range=(last_7_days, today)).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_7_days_wear_income = last_7_days_wear_income.get('xo')

    # Last 7 days Finance income
    last_7_days_finance_income = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__range=(last_7_days, today)).aggregate(yo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_7_days_finance_income = last_7_days_finance_income.get('yo')

    # sum all last_7_days income together  last_3_days_finance_count
    sum_last_7_days_income = last_7_days_wear_income + last_7_days_finance_income


    # last 7 days wear expenses
    last_7_days_wear_expenses = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__range=(last_7_days, today)).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_7_days_wear_expenses = last_7_days_wear_expenses.get('xo')

    # last 7 days finance expenses
    last_7_days_finance_expenses = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__range=(last_7_days, today)).aggregate(uo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_7_days_finance_expenses = last_7_days_finance_expenses.get('uo')

    # sum all last_7_days expenses together  
    sum_last_7_days_expenses = last_7_days_wear_expenses + last_7_days_finance_expenses


    # summing amount for last 7 days
    total_amount_for_last_7_days = sum_last_7_days_income + sum_last_7_days_expenses

    # Last 7 days wear total amount
    last_7_days_wear_total_amount = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_7_days, today)).aggregate(ho=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_7_days_wear_total_amount = last_7_days_wear_total_amount.get('ho')


    # Last 7 days finance total amount
    last_7_days_finance_total_amount = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__range=(last_7_days, today)).aggregate(zo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    last_7_days_finance_total_amount = last_7_days_finance_total_amount.get('zo')




    context = {
        # counting last 7 days income data for both wears and finance and summing them together
        'last_7_days_wear_income_count': last_7_days_wear_income_count,
        'last_7_days_finance_income_count': last_7_days_finance_income_count,
        'income_for_last_7_days': income_for_last_7_days,

        # counting last 7 days expenses data for both wears and finance and summing them together
        'last_7_days_wear_expenses_count': last_7_days_wear_expenses_count,
        'last_7_days_finance_expenses_count': last_7_days_finance_expenses_count,
        'expenses_for_last_7_days': expenses_for_last_7_days,


        # last 7 days data count
        'last_7_days_wear_count': last_7_days_wear_count,    # counting all wear for the last 7 days
        'last_7_days_finance_count': last_7_days_finance_count, # counting all finance for the last 7 days
        'last_7_days_data_count': last_7_days_data_count,    # summing all of the to get the total data for the last 7 days

        # last 7 days income for both wear and finance
        'last_7_days_wear_income': last_7_days_wear_income,
        'last_7_days_finance_income': last_7_days_finance_income,
        'sum_last_7_days_income': sum_last_7_days_income,

        # last 7 days expenses for both wear and finance
        'last_7_days_wear_expenses': last_7_days_wear_expenses,
        'last_7_days_finance_expenses': last_7_days_finance_expenses,
        'sum_last_7_days_expenses': sum_last_7_days_expenses,

        # total amount for last 7 days
        'total_amount_for_last_7_days': total_amount_for_last_7_days,
        

        # last_7_days_wear_total_amount
        'last_7_days_wear_total_amount': last_7_days_wear_total_amount,
        
        # last_7_days_finance_total_amount
        'last_7_days_finance_total_amount': last_7_days_finance_total_amount,


    }
    return render(request, 'homapp/finance/last_7_days.html', context)




# Current week summary 
@login_required 
def current_week(request):


    current_date = timezone.now()
    current_year, current_week, current_weekday = current_date.isocalendar()
    

    # counting current week wear income alone
    current_week_wear_income_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__week=current_week).count()


     # counting current week wear income alone
    current_week_finance_income_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__week=current_week).count()


    # summing up current week income from both wears and finance together
    income_for_current_week = current_week_wear_income_count + current_week_finance_income_count




    # counting current week wear expenses alone  
    current_week_wear_expenses_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__week=current_week).count()


    # counting current week finance expenses alone
    current_week_finance_expenses_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__week=current_week).count()


    # summing up current week expenses from both wears and finance together
    expenses_for_current_week = current_week_wear_expenses_count + current_week_finance_expenses_count




    current_week_wear_count = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__week=current_week).count()


    current_week_finance_count = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__week=current_week).count()


    # summing total data for current week   
    current_week_data_count = current_week_wear_count + current_week_finance_count  


    # current week wear income
    current_week_wear_income = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__week=current_week).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_week_wear_income = current_week_wear_income.get('xo')

    # current week Finance income
    current_week_finance_income = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__week=current_week).aggregate(yo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_week_finance_income = current_week_finance_income.get('yo')

    # sum all current week income together and all current week finance_count
    sum_current_week_income = current_week_wear_income + current_week_finance_income 



    # current week wear expenses
    current_week_wear_expenses = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__week=current_week).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_week_wear_expenses = current_week_wear_expenses.get('xo')

    # current week finance expenses
    current_week_finance_expenses = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__week=current_week).aggregate(uo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_week_finance_expenses = current_week_finance_expenses.get('uo')

    # sum all current week expenses together  
    sum_current_week_expenses = current_week_wear_expenses + current_week_finance_expenses



    # summing amount for current week
    total_amount_for_current_week = sum_current_week_income + sum_current_week_expenses

    # This current week wear total amount
    current_week_wear_total_amount = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__week=current_week).aggregate(ho=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_week_wear_total_amount = current_week_wear_total_amount.get('ho')


    # This current week finance total amount
    current_week_finance_total_amount = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__week=current_week).aggregate(zo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_week_finance_total_amount = current_week_finance_total_amount.get('zo')



    context = {
        # counting current week income data for both wears and finance and summing them together
        'current_week_wear_income_count': current_week_wear_income_count,
        'current_week_finance_income_count': current_week_finance_income_count,
        'income_for_current_week': income_for_current_week,

        # counting current week expenses data for both wears and finance and summing them together
        'current_week_wear_expenses_count': current_week_wear_expenses_count,
        'current_week_finance_expenses_count': current_week_finance_expenses_count,
        'expenses_for_current_week': expenses_for_current_week,


        # current week data count
        'current_week_wear_count': current_week_wear_count,    # counting all wear for the last 7 days
        'current_week_finance_count': current_week_finance_count, # counting all finance for the last 7 days
        'current_week_data_count': current_week_data_count,    # summing all of the to get the total data for the last 7 days

        # current week income for both wear and finance
        'current_week_wear_income': current_week_wear_income,
        'current_week_finance_income': current_week_finance_income,
        'sum_current_week_income': sum_current_week_income,

        # current week expenses for both wear and finance
        'current_week_wear_expenses': current_week_wear_expenses,
        'current_week_finance_expenses': current_week_finance_expenses,
        'sum_current_week_expenses': sum_current_week_expenses,

        # total amount for current week
        'total_amount_for_current_week': total_amount_for_current_week,

        'current_week': current_week,

        # To sum the current week total amount
        'current_week_wear_total_amount':  current_week_wear_total_amount,
        'current_week_finance_total_amount': current_week_finance_total_amount,


    }
    return render(request, 'homapp/finance/current_week.html', context)




# Current month summary  
@login_required
def current_month(request):


    current_date = timezone.now()
    current_month = current_date.month
    

    # counting last 7 days wear income alone
    current_month_wear_income_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__month=current_month).count()


     # counting last 7 days wear income alone
    current_month_finance_income_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__month=current_month).count()


    # summing up last 7 days income from both wears and finance together
    income_for_current_month = current_month_wear_income_count + current_month_finance_income_count




    # counting last 7 days wear expenses alone  
    current_month_wear_expenses_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__month=current_month).count()


    # counting last 7 days finance expenses alone
    current_month_finance_expenses_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__month=current_month).count()


    # summing up last 7 days expenses from both wears and finance together
    expenses_for_current_month = current_month_wear_expenses_count + current_month_finance_expenses_count




    current_month_wear_count = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__month=current_month).count()


    current_month_finance_count = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__month=current_month).count()


    # summing total data for last 7 days   
    current_month_data_count = current_month_wear_count + current_month_finance_count  


    # Last 7 days wear income
    current_month_wear_income = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__month=current_month).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_month_wear_income = current_month_wear_income.get('xo')

    # Last 7 days Finance income
    current_month_finance_income = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__month=current_month).aggregate(yo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_month_finance_income = current_month_finance_income.get('yo')

    # sum all last_7_days income together  last_3_days_finance_count
    sum_current_month_income = current_month_wear_income + current_month_finance_income 



    # last 7 days wear expenses
    current_month_wear_expenses = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__month=current_month).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_month_wear_expenses = current_month_wear_expenses.get('xo')

    # last 7 days finance expenses
    current_month_finance_expenses = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__month=current_month).aggregate(uo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_month_finance_expenses = current_month_finance_expenses.get('uo')

    # sum all last_7_days expenses together  
    sum_current_month_expenses = current_month_wear_expenses + current_month_finance_expenses



    # summing amount for last 7 days
    total_amount_for_current_month = sum_current_month_income + sum_current_month_expenses

    # This month wear total amount
    current_month_wear_total_amount = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__month=current_month).aggregate(ho=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_month_wear_total_amount = current_month_wear_total_amount.get('ho')


    # This month finance total amount
    current_month_finance_total_amount = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__month=current_month).aggregate(zo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_month_finance_total_amount = current_month_finance_total_amount.get('zo')



    context = {
        # counting last 7 days income data for both wears and finance and summing them together
        'current_month_wear_income_count': current_month_wear_income_count,
        'current_month_finance_income_count': current_month_finance_income_count,
        'income_for_current_month': income_for_current_month,

        # counting last 7 days expenses data for both wears and finance and summing them together
        'current_month_wear_expenses_count': current_month_wear_expenses_count,
        'current_month_finance_expenses_count': current_month_finance_expenses_count,
        'expenses_for_current_month': expenses_for_current_month,


        # last 7 days data count
        'current_month_wear_count': current_month_wear_count,    # counting all wear for the last 7 days
        'current_month_finance_count': current_month_finance_count, # counting all finance for the last 7 days
        'current_month_data_count': current_month_data_count,    # summing all of the to get the total data for the last 7 days

        # last 7 days income for both wear and finance
        'current_month_wear_income': current_month_wear_income,
        'current_month_finance_income': current_month_finance_income,
        'sum_current_month_income': sum_current_month_income,

        # last 7 days expenses for both wear and finance
        'current_month_wear_expenses': current_month_wear_expenses,
        'current_month_finance_expenses': current_month_finance_expenses,
        'sum_current_month_expenses': sum_current_month_expenses,

        # total amount for last 7 days
        'total_amount_for_current_month': total_amount_for_current_month,

        'current_month': current_month,

        # To sum the current month total amount
        'current_month_wear_total_amount':  current_month_wear_total_amount,
        'current_month_finance_total_amount': current_month_finance_total_amount,


    }
    return render(request, 'homapp/finance/current_month.html', context)





# Current month summary  
@login_required
def current_year(request):
    

    current_date = timezone.now()
    current_year = current_date.year
    

    # counting this year wear income alone
    current_year_wear_income_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__year=current_year).count()


     # counting this year wear income alone
    current_year_finance_income_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__year=current_year).count()


    # summing up this year income from both wears and finance together
    income_for_current_year = current_year_wear_income_count + current_year_finance_income_count




    # counting this year wear expenses alone  
    current_year_wear_expenses_count = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__year=current_year).count()


    # counting this year finance expenses alone
    current_year_finance_expenses_count = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__year=current_year).count()


    # summing up this year expenses from both wears and finance together
    expenses_for_current_year = current_year_wear_expenses_count + current_year_finance_expenses_count




    current_year_wear_count = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__year=current_year).count()


    current_year_finance_count = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__year=current_year).count()


    # summing total data for this year   
    current_year_data_count = current_year_wear_count + current_year_finance_count  


    # this year wear income
    current_year_wear_income = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__year=current_year).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_year_wear_income = current_year_wear_income.get('xo')

    # this year Finance income
    current_year_finance_income = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=False, date_created__year=current_year).aggregate(yo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_year_finance_income = current_year_finance_income.get('yo')

    # sum all this year income together  last_3_days_finance_count
    sum_current_year_income = current_year_wear_income + current_year_finance_income 



    # this year wear expenses
    current_year_wear_expenses = Wear.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__year=current_year).aggregate(xo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_year_wear_expenses = current_year_wear_expenses.get('xo')

    # this year finance expenses
    current_year_finance_expenses = Finance.objects.filter(user_id=request.user.id, activate=True, expenses=True, date_created__year=current_year).aggregate(uo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_year_finance_expenses = current_year_finance_expenses.get('uo')

    # sum all this year expenses together  
    sum_current_year_expenses = current_year_wear_expenses + current_year_finance_expenses



    # summing amount for this year
    total_amount_for_current_year = sum_current_year_income + sum_current_year_expenses

    # This year wear total amount
    current_year_wear_total_amount = Wear.objects.filter(user_id=request.user.id, activate=True, date_created__year=current_year).aggregate(ho=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_year_wear_total_amount = current_year_wear_total_amount.get('ho')


    # This year finance total amount
    current_year_finance_total_amount = Finance.objects.filter(user_id=request.user.id, activate=True, date_created__year=current_year).aggregate(zo=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    current_year_finance_total_amount = current_year_finance_total_amount.get('zo')



    context = {
        # counting this year income data for both wears and finance and summing them together
        'current_year_wear_income_count': current_year_wear_income_count,
        'current_year_finance_income_count': current_year_finance_income_count,
        'income_for_current_year': income_for_current_year,

        # counting this year expenses data for both wears and finance and summing them together
        'current_year_wear_expenses_count': current_year_wear_expenses_count,
        'current_year_finance_expenses_count': current_year_finance_expenses_count,
        'expenses_for_current_year': expenses_for_current_year,


        # this year data count
        'current_year_wear_count': current_year_wear_count,    # counting all wear for the last 7 days
        'current_year_finance_count': current_year_finance_count, # counting all finance for the last 7 days
        'current_year_data_count': current_year_data_count,    # summing all of the to get the total data for the last 7 days

        # this year income for both wear and finance
        'current_year_wear_income': current_year_wear_income,
        'current_year_finance_income': current_year_finance_income,
        'sum_current_year_income': sum_current_year_income,

        # this year expenses for both wear and finance
        'current_year_wear_expenses': current_year_wear_expenses,
        'current_year_finance_expenses': current_year_finance_expenses,
        'sum_current_year_expenses': sum_current_year_expenses,

        # total amount for this year
        'total_amount_for_current_year': total_amount_for_current_year,

        'current_year': current_year,

        # To sum the current year total amount
        'current_year_wear_total_amount':  current_year_wear_total_amount,
        'current_year_finance_total_amount': current_year_finance_total_amount,


    }
    return render(request, 'homapp/finance/current_year.html', context)




# Todo app list view 
@login_required 
def list_task(request):
    count_task_filtered = None
    selected_task_category = None
    
    all_task = Task.objects.filter(user_id=request.user.id, activate=True).order_by( 'complete', 'due')

    # This particular database query is for pagination purposes only...
    # hmm = Task.objects.filter(user_id=request.user.id, activate=True).order_by('complete', 'due')

    # for pagination logic
    # paginator = Paginator(all_task, 10)
    # page = request.GET.get('page', 1)

    # try:
    #     all_task = paginator.page(page)
    # except PageNotAnInteger:
    #     all_task = paginator.page(1)
    # except EmptyPage:
    #     all_task = paginator.page(paginator.num_pages)



    todo_form = TodoForm(request.user)
    if request.method == 'POST':
        todo_form = TodoForm(request.user, request.POST)
        if todo_form.is_valid():
            add_user = todo_form.save(commit=False)
            add_user.user_id = request.user.id
            add_user.save()
            todo_form = TodoForm(request.user)
            messages.success(request, 'Task added successfully'.title())
            return redirect('homapp:list_task')
    

    # counting all tasks 
    all_task_count = Task.objects.filter(user_id=request.user.id, activate=True)

    # Counting all uncompleted Tasks
    uncompleted_tasks = Task.objects.filter(user_id=request.user.id, activate=True, complete=False).count()

    # counting all completed tasks
    completed_tasks = Task.objects.filter(user_id=request.user.id, activate=True, complete=True).count()

    # All deactivated tasks
    deactivated_tasks = Task.objects.filter(user_id=request.user.id, activate=False).count()

    # Task categories
    task_categories = TaskCategory.objects.filter(user_id=request.user.id, activate=True)

    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    completed = request.GET.get('completed')
    not_completed = request.GET.get('not_completed')
    search = request.GET.get('search')

    if category != '' and category != None and category != 'Choose...':
        all_task = all_task.filter(category_id=category)
        count_task_filtered = all_task.filter(category_id=category)
        selected_task_category = get_object_or_404(TaskCategory, id=category)
    
    if start_date != '' and start_date != None:
        all_task = all_task.filter(date_created__gte=start_date)
        count_task_filtered = all_task.filter(date_created__gte=start_date)
        
    
    if end_date != '' and end_date != None:
        all_task = all_task.filter(date_created__lt=end_date)
        count_task_filtered = all_task.filter(date_created__lt=end_date)
    
    if search != '' and search != None: 
        all_task = all_task.filter(name__icontains=search)
        count_task_filtered = all_task.filter(name__icontains=search)
    
    if completed == 'on':
        all_task = all_task.filter(complete=True)
        count_task_filtered = all_task.filter(complete=True)
       

    elif not_completed == 'on':
        all_task = all_task.filter(complete=False)
        count_task_filtered = all_task.filter(complete=False)
        

   



    context = {
        'all_task': all_task,
        'todo_form': todo_form,
        'all_task_count': all_task_count,
        'uncompleted_tasks': uncompleted_tasks,
        'completed_tasks': completed_tasks,
        'deactivated_tasks': deactivated_tasks,
        'task_categories': task_categories,
        'count_task_filtered': count_task_filtered,
        'selected_task_category': selected_task_category,
        # 'hmm': hmm,
    }
    return render(request, 'homapp/todo/list_task.html', context)

@login_required
def update_todo_task(request, pk):
    qs = get_object_or_404(Task, activate=True,  id=pk, user_id=request.user.id)
    todo_update_form = UpdateTodoForm(request.user, instance=qs)
    # Processing the data inside the form
    if request.method == 'POST':
        todo_update_form = UpdateTodoForm(request.user, request.POST, instance=qs)
        if todo_update_form.is_valid():
            add_user = todo_update_form.save(commit=False)
            add_user.user_id = request.user.id
            add_user.save()
            messages.success(request, 'task updated successfully'.title())
            return redirect('homapp:list_task')

    context = {
        'todo_update_form': todo_update_form,
    }
    return render(request, 'homapp/todo/update_todo_form.html', context)

@login_required
def delete_task(request, pk):
    qs = get_object_or_404(Task, id=pk, user_id=request.user.id)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f'{qs.name} was deleted successfully'.title())
        return redirect('homapp:list_task')
    context = {
        'qs': qs,
    }
    return render(request, 'homapp/todo/delete_task.html', context)

@login_required
def task_detail(request, pk):
    duration = None
    qs = get_object_or_404(Task, id=pk, user_id=request.user.id)

    # Trying to calculate the duration its takes each task to be completed
    if qs.date_updated and qs.complete == True:
        date_created = qs.date_created
        date_updated = qs.date_updated
        duration = date_updated - date_created

    context = {
        'qs': qs,
        'duration': duration,
    }
    return render(request, 'homapp/todo/task_detail.html', context)





@login_required 
def list_task_category(request):
    count_task_filtered = None
    selected_task_category = None
    
    all_task_category = TaskCategory.objects.filter(user_id=request.user.id, activate=True).order_by('-date_created')
    deactivated_task_categories = TaskCategory.objects.filter(user_id=request.user.id, activate=False).order_by('-date_created').count()
    

    add_task_category_form = TaskCategoryForm()
    if request.method == 'POST':
        add_task_category_form = TaskCategoryForm(request.POST)
        if add_task_category_form.is_valid():
            add_user = add_task_category_form.save(commit=False)
            add_user.user_id = request.user.id
            add_user.save()
            add_task_category_form = TaskCategoryForm()
            messages.success(request, f'{add_user.name} was created successfully'.title())
            return redirect('homapp:list_task_category')
    

    

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search = request.GET.get('search')


    if start_date != '' and start_date != None:
        all_task_category = all_task_category.filter(activate=True, user_id=request.user.id, date_created__gte=start_date)
        count_task_filtered = all_task_category.filter(activate=True, user_id=request.user.id, date_created__gte=start_date)
        
    
    if end_date != '' and end_date != None:
        all_task_category = all_task_category.filter(activate=True, user_id=request.user.id, date_created__lt=end_date)
        count_task_filtered = all_task_category.filter(activate=True, user_id=request.user.id, date_created__lt=end_date)
    
    if search != '' and search != None: 
        all_task_category = all_task_category.filter(activate=True, user_id=request.user.id, name__icontains=search)
        count_task_filtered = all_task_category.filter(activate=True, user_id=request.user.id, name__icontains=search)
    
    # last added task category
    last_added_task_category = TaskCategory.objects.filter(user_id=request.user.id, activate=True).order_by('-date_created')[:1]


    
    

    context = {
        'all_task_category': all_task_category,
        'add_task_category_form': add_task_category_form,
        'deactivated_task_categories': deactivated_task_categories,
        'count_task_filtered': count_task_filtered,
        'last_added_task_category': last_added_task_category,
    }
    return render(request, 'homapp/todo/add_task_category.html', context)


# update task category 
@login_required
def update_task_category(request, pk):
    qs = get_object_or_404(TaskCategory, activate=True, id=pk, user_id=request.user.id)
    update_task_category_form = UpdateTaskCategoryForm(instance=qs)
    if request.method == 'POST':
        update_task_category_form = UpdateTaskCategoryForm(request.POST, instance=qs)
        if update_task_category_form.is_valid():
            add_user = update_task_category_form.save(commit=False)
            add_user.user_id = request.user.id  
            add_user.save()
            messages.success(request, f'{add_user.name} was updated successfully'.title())
            return redirect('homapp:list_task_category')

    context = {
        'update_task_category_form': update_task_category_form,
    }
    return render(request, 'homapp/todo/update_task_category.html', context)

# delete task category  
@login_required
def delete_task_category(request, pk):
    qs = get_object_or_404(TaskCategory, id=pk, user_id=request.user.id)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f'{qs.name} was deleted successfully'.title())
        return redirect('homapp:list_task_category')
    context = {
        'qs': qs,
    }
    return render(request, 'homapp/todo/delete_task_category.html', context)


# Task deactivated view
@login_required 
def deactivated_task(request):
    count_task_filtered = None
    selected_task_category = None
    
    all_deactivated_task = Task.objects.filter(user_id=request.user.id, activate=False).order_by( 'complete', 'due')

    todo_form = TodoForm(request.user)
    if request.method == 'POST':
        todo_form = TodoForm(request.user, request.POST)
        if todo_form.is_valid():
            add_user = todo_form.save(commit=False)
            add_user.user_id = request.user.id
            add_user.save()
            todo_form = TodoForm()
            messages.success(request, 'Task added successfully'.title())
            return redirect('homapp:list_task')
    

    # counting all tasks 
    all_deactivated_task_count = Task.objects.filter(user_id=request.user.id, activate=False)

    # Counting all uncompleted Tasks
    uncompleted_deactivated_tasks = Task.objects.filter(user_id=request.user.id, activate=False, complete=False).count()

    # counting all completed tasks
    completed_deactivated_tasks = Task.objects.filter(user_id=request.user.id, activate=False, complete=True).count()

    # All deactivated tasks
    activated_tasks = Task.objects.filter(user_id=request.user.id, activate=True).count()

    # Task categories
    task_categories = TaskCategory.objects.filter(user_id=request.user.id, activate=True)

    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    completed = request.GET.get('completed')
    not_completed = request.GET.get('not_completed')
    search = request.GET.get('search')

    if category != '' and category != None and category != 'Choose...':
        all_deactivated_task = all_deactivated_task.filter(category_id=category)
        count_task_filtered = all_deactivated_task.filter(category_id=category)
        selected_task_category = get_object_or_404(TaskCategory, id=category)
    
    if start_date != '' and start_date != None:
        all_deactivated_task = all_deactivated_task.filter(date_created__gte=start_date)
        count_task_filtered = all_deactivated_task.filter(date_created__gte=start_date)
        
    
    if end_date != '' and end_date != None:
        all_deactivated_task = all_deactivated_task.filter(date_created__lt=end_date)
        count_task_filtered = all_deactivated_task.filter(date_created__lt=end_date)
    
    if search != '' and search != None: 
        all_deactivated_task = all_deactivated_task.filter(name__icontains=search)
        count_task_filtered = all_deactivated_task.filter(name__icontains=search)
    
    if completed == 'on':
        all_deactivated_task = all_deactivated_task.filter(complete=True)
        count_task_filtered = all_deactivated_task.filter(complete=True)
       

    elif not_completed == 'on':
        all_deactivated_task = all_deactivated_task.filter(complete=False)
        count_task_filtered = all_deactivated_task.filter(complete=False)
        




    context = {
        'all_deactivated_task': all_deactivated_task,
        'todo_form': todo_form,
        'all_deactivated_task_count': all_deactivated_task_count,
        'uncompleted_deactivated_tasks': uncompleted_deactivated_tasks,
        'completed_deactivated_tasks': completed_deactivated_tasks,
        'activated_tasks': activated_tasks,
        'task_categories': task_categories,
        'count_task_filtered': count_task_filtered,
        'selected_task_category': selected_task_category,
    }
    return render(request, 'homapp/todo/deactivated_task.html', context)


# Update deactivated task
@login_required
def update_todo_task_deactivated(request, pk):  
    qs = get_object_or_404(Task, activate=False,  id=pk)
    todo_update_form = UpdateTodoForm(request.user, instance=qs)
    # Processing the data inside the form
    if request.method == 'POST':
        todo_update_form = UpdateTodoForm(request.user, request.POST,instance=qs)
        if todo_update_form.is_valid():
            add_user = todo_update_form.save(commit=False)
            add_user.user_id = request.user.id
            add_user.save()
            messages.success(request, 'task updated successfully'.title())
            return redirect('homapp:deactivated_task')

    context = {
        'todo_update_form': todo_update_form,
    }
    return render(request, 'homapp/todo/update_todo_form.html', context)

# All task deactivated categories
@login_required 
def deactivated_task_category(request):
    count_task_filtered = None
    selected_task_category = None
    
    all_deactivated_task_category = TaskCategory.objects.filter(user_id=request.user.id, activate=False).order_by('-date_created')
    activated_task_categories = TaskCategory.objects.filter(user_id=request.user.id, activate=True).order_by('-date_created').count()
    

    add_task_category_form = TaskCategoryForm()
    if request.method == 'POST':
        add_task_category_form = TaskCategoryForm(request.POST)
        if add_task_category_form.is_valid():
            add_user = add_task_category_form.save(commit=False)
            add_user.user_id = request.user.id
            add_user.save()
            add_task_category_form = TaskCategoryForm()
            messages.success(request, f'{add_user.name} was created successfully'.title())
            return redirect('homapp:list_task_category')
    

    

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search = request.GET.get('search')


    if start_date != '' and start_date != None:
        all_deactivated_task_category = all_deactivated_task_category.filter(activate=False, user_id=request.user.id, date_created__gte=start_date)
        count_task_filtered = all_deactivated_task_category.filter(activate=False, user_id=request.user.id, date_created__gte=start_date)
        
    
    if end_date != '' and end_date != None:
        all_deactivated_task_category = all_deactivated_task_category.filter(activate=False, user_id=request.user.id, date_created__lt=end_date)
        count_task_filtered = all_deactivated_task_category.filter(activate=False, user_id=request.user.id, date_created__lt=end_date)
    
    if search != '' and search != None: 
        all_deactivated_task_category = all_deactivated_task_category.filter(activate=False, user_id=request.user.id, name__icontains=search)
        count_task_filtered = all_deactivated_task_category.filter(activate=False, user_id=request.user.id, name__icontains=search)
    
    # last added task category
    last_added_task_category = TaskCategory.objects.filter(user_id=request.user.id, activate=True).order_by('-date_created')[:1]


    
    

    context = {
        'all_deactivated_task_category': all_deactivated_task_category,
        'add_task_category_form': add_task_category_form,
        'activated_task_categories': activated_task_categories,
        'count_task_filtered': count_task_filtered,
        'last_added_task_category': last_added_task_category,
    }
    return render(request, 'homapp/todo/all_deactivated_task_category.html', context)

# update task deactivated category 
@login_required
def update_task_deactivated_category(request, pk): 
    qs = get_object_or_404(TaskCategory, activate=False, id=pk, user_id=request.user.id)
    update_task_category_form = UpdateTaskCategoryForm(instance=qs)
    if request.method == 'POST':
        update_task_category_form = UpdateTaskCategoryForm(request.POST, instance=qs)
        if update_task_category_form.is_valid():
            add_user = update_task_category_form.save(commit=False)
            add_user.user_id = request.user.id  
            add_user.save()
            messages.success(request, f'{add_user.name} was updated successfully'.title())
            return redirect('homapp:deactivated_task_category')

    context = {
        'update_task_category_form': update_task_category_form,
    }
    return render(request, 'homapp/todo/update_task_category.html', context)




# Admin views only
@login_required
@only_admin
def all_wears_for_admin(request):
    count_with_data_selected = None

    all_wears_for_admin = Wear.objects.all()
    total_users = User.objects.all()
    total_wears_categories = WearCategory.objects.all()
    total_deactivated_wears = Wear.objects.filter(activate=False)
    categories = WearCategory.objects.all()


    # getting the names from the form
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = request.GET.get('expenses')
    not_expenses = request.GET.get('not_expenses')
    search = request.GET.get('search')

    
    if category != '' and category != None and category != 'Choose...':
        all_wears_for_admin = all_wears_for_admin.filter(category_id=category)
        count_with_data_selected = all_wears_for_admin.filter(category_id=category)
        selected_category = get_object_or_404(WearCategory, id=category)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table

        
       
    
    if start_date != '' and start_date != None:
        all_wears_for_admin = all_wears_for_admin.filter(date_created__gte=start_date)
        count_with_data_selected = all_wears_for_admin.filter(date_created__gte=start_date)

    

    if end_date != '' and end_date != None:
        all_wears_for_admin = all_wears_for_admin.filter(date_created__lt=end_date)
        count_with_data_selected = all_wears_for_admin.filter(date_created__lt=end_date)


    
    if search != '' and search != None: 
        all_wears_for_admin = all_wears_for_admin.filter(user__username__icontains=search)
        count_with_data_selected = all_wears_for_admin.filter(user__username__icontains=search)

        
    
    if expenses == 'on':
        all_wears_for_admin = all_wears_for_admin.filter(expenses=True)
        count_with_data_selected = all_wears_for_admin.filter(expenses=True)
        
        
    elif not_expenses == 'on':
        all_wears_for_admin = all_wears_for_admin.filter(expenses=False)
        count_with_data_selected = all_wears_for_admin.filter(expenses=False)

    context = {
        'all_wears_for_admin': all_wears_for_admin,
        'total_users': total_users,
        'total_wears_categories': total_wears_categories,
        'total_deactivated_wears': total_deactivated_wears,
        'categories': categories,
        'count_with_data_selected': count_with_data_selected,
    }
    return render(request, 'homapp/for_admin/all_wears_for_admin.html', context)



# Only Admin users will be able to edit wear here
@login_required
@only_admin
def admin_edit_wear(request, pk):
    qs = get_object_or_404(Wear, id=pk)
    admin_edit_wear_form = AdminEditWearForm(instance=qs)
    if request.method == 'POST':
        admin_edit_wear_form = AdminEditWearForm(request.POST, instance=qs)
        if admin_edit_wear_form.is_valid():
            get_user_username = admin_edit_wear_form.save(commit=False)
            get_user_username.save()
            messages.success(request, f'wear for {get_user_username.user.username} was updated successfully')
            return redirect('homapp:all_wears_for_admin')

    context = {
        'qs': qs, 
        'admin_edit_wear_form': admin_edit_wear_form,
    }
    return render(request, 'homapp/for_admin/admin_edit_wear.html', context)


# Only admin users will be able to delete any wear 
@login_required
@only_admin
def admin_delete_wear(request, pk):
    qs = get_object_or_404(Wear, id=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f'wear was deleted successfully for {qs.user.username}')
        return redirect('homapp:all_wears_for_admin')

    context = {
        'qs': qs,
    }
    return render(request, 'homapp/for_admin/admin_delete_wear.html', context)



# Only admin users to see all wear categories from all users
@login_required
@only_admin
def all_wears_categories_for_admin(request):
    count_with_data_selected = None

    all_wears_for_admin = Wear.objects.all()
    """ i am using values_list and adding flat=True and .distinct() so that i can get only the owners of each category and count them, 
    remember that a single user can have many categories created by only him/her, so i needed a way to count only those 
    categories creators only """
    total_users_category_owner = WearCategory.objects.values_list('category_owner', flat=True).distinct()
    total_wears_categories = WearCategory.objects.all()
    total_deactivated_wears_categories = WearCategory.objects.filter(activate=False)

    # for my filter categories selection
    categories = WearCategory.objects.all()


    # getting the names from the form
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    activated = request.GET.get('activated')
    not_activated = request.GET.get('not_activated')
    search = request.GET.get('search')


    if start_date != '' and start_date != None:
        total_wears_categories = total_wears_categories.filter(date_created__gte=start_date)
        count_with_data_selected = total_wears_categories.filter(date_created__gte=start_date)

    

    if end_date != '' and end_date != None:
        total_wears_categories = total_wears_categories.filter(date_created__lt=end_date)
        count_with_data_selected = total_wears_categories.filter(date_created__lt=end_date)


    
    if search != '' and search != None: 
        total_wears_categories = total_wears_categories.filter(category_name__icontains=search)
        count_with_data_selected = total_wears_categories.filter(category_name__icontains=search)

        
    
    if activated == 'on':
        total_wears_categories = total_wears_categories.filter(activate=True)
        count_with_data_selected = total_wears_categories.filter(activate=True)
        
        
    elif not_activated == 'on':
        total_wears_categories = total_wears_categories.filter(activate=False)
        count_with_data_selected = total_wears_categories.filter(activate=False)

    context = {
        'all_wears_for_admin': all_wears_for_admin,
        'total_users_category_owner': total_users_category_owner,
        'total_wears_categories': total_wears_categories,
        'total_deactivated_wears_categories': total_deactivated_wears_categories,
        'count_with_data_selected': count_with_data_selected,

        'categories': categories,
    }
    return render(request, 'homapp/for_admin/all_wears_categories_for_admin.html', context)

# Only admin will be able to add wear category for any user
@login_required
@only_admin
def admin_add_wear_category(request):
    admin_add_wear_category_form = AdminAddWearCategoryForm()
    if request.method == 'POST':
        admin_add_wear_category_form = AdminAddWearCategoryForm(request.POST)
        if admin_add_wear_category_form.is_valid():
            get_user_username = admin_add_wear_category_form.save(commit=False)
            get_user_username.save()
            messages.success(request, f'{get_user_username.category_name} wear category was added successfully for {get_user_username.category_owner.username}')
            return redirect('homapp:all_wears_categories_for_admin')


    context = {
        'admin_add_wear_category_form': admin_add_wear_category_form,
    }
    return render(request, 'homapp/for_admin/admin_add_wear_category.html', context)


# Admin to edit wear category for any user
@login_required
@only_admin
def admin_edit_wear_category(request, pk):
    qs = get_object_or_404(WearCategory, id=pk)
    admin_edit_wear_category_form = AdminEditWearCategoryForm(instance=qs)
    if request.method == 'POST': 
        admin_edit_wear_category_form = AdminEditWearCategoryForm(request.POST, instance=qs)
        if admin_edit_wear_category_form.is_valid():
            get_user_username = admin_edit_wear_category_form.save(commit=False)
            get_user_username.save()
            messages.success(request, f'{get_user_username.category_name} category was updated successfully for { get_user_username.category_owner.username }')
            return redirect('homapp:all_wears_categories_for_admin')

    context = {
        'qs': qs, 
        'admin_edit_wear_category_form': admin_edit_wear_category_form,
    }
    return render(request, 'homapp/for_admin/admin_edit_wear_category.html', context)



# Admin delete wear category
@login_required
@only_admin
def admin_delete_wear_category(request, pk):
    qs = get_object_or_404(WearCategory, id=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f'{qs.category_name} category was deleted successfully for {qs.category_owner.username }')
        return redirect('homapp:all_wears_categories_for_admin')

    context = {
        'qs': qs,
    }
    return render(request, 'homapp/for_admin/admin_delete_wear_category.html', context )


# Admin views only to see all finance
@login_required
@only_admin
def all_finance_for_admin(request):
    count_with_data_selected = None

    all_finance_for_admin = Finance.objects.all()
    total_users_for_admin = User.objects.all()
    total_finance_categories = FinanceCategory.objects.all()
    total_deactivated_finance = Finance.objects.filter(activate=False)
    categories = FinanceCategory.objects.all()

    total_amount_for_finance = Finance.objects.all().aggregate(p=Coalesce(Sum('amount'), V(0), output_field=DecimalField()))
    total_amount_for_finance = total_amount_for_finance.get('p')


 

    # getting the names from the form
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = request.GET.get('expenses')
    not_expenses = request.GET.get('not_expenses')
    activated = request.GET.get('activated')
    not_activated = request.GET.get('not_activated')
    search = request.GET.get('search')

    
    if category != '' and category != None and category != 'Choose...':
        all_finance_for_admin = all_finance_for_admin.filter(category_id=category)
        count_with_data_selected = all_finance_for_admin.filter(category_id=category)
        selected_category = get_object_or_404(WearCategory, id=category)  # i grab the value of the category selected above and push it in for category table using the id and from here, i can access all the atribute of the wearcategory table

        
       
    
    if start_date != '' and start_date != None:
       all_finance_for_admin = all_finance_for_admin.filter(date_created__gte=start_date)
       count_with_data_selected = all_finance_for_admin.filter(date_created__gte=start_date)

    

    if end_date != '' and end_date != None:
        all_finance_for_admin = all_finance_for_admin.filter(date_created__lt=end_date)
        count_with_data_selected = all_finance_for_admin.filter(date_created__lt=end_date)


    
    if search != '' and search != None: 
        all_finance_for_admin = all_finance_for_admin.filter(user__username__icontains=search)
        count_with_data_selected = all_finance_for_admin.filter(user__username__icontains=search)

        
    
    if expenses == 'on':
        all_finance_for_admin = all_finance_for_admin.filter(expenses=True)
        count_with_data_selected =all_finance_for_admin.filter(expenses=True)
        
        
    if not_expenses == 'on':
        all_finance_for_admin = all_finance_for_admin.filter(expenses=False)
        count_with_data_selected = all_finance_for_admin.filter(expenses=False)

    if activated == 'on':
        all_finance_for_admin = all_finance_for_admin.filter(activate=True)
        count_with_data_selected =all_finance_for_admin.filter(activate=True)
        
        
    elif not_activated == 'on':
        all_finance_for_admin = all_finance_for_admin.filter(activate=False)
        count_with_data_selected = all_finance_for_admin.filter(activate=False)

    context = {
        'all_finance_for_admin': all_finance_for_admin,
        'total_users_for_admin': total_users_for_admin,
        'total_finance_categories': total_finance_categories,
        'total_deactivated_finance': total_deactivated_finance,
        'categories': categories,
        'count_with_data_selected': count_with_data_selected,
        'total_amount_for_finance': total_amount_for_finance,
    }
    return render(request, 'homapp/for_admin/all_finance_for_admin.html', context)


@login_required
@only_admin
def admin_add_finance(request):
    finance_for_user = None
    admin_add_finance_form = AdminAddFinanceForm()
    if request.method == 'POST':
        admin_add_finance_form = AdminAddFinanceForm(request.POST, request.FILES)
        if admin_add_finance_form.is_valid():
            finance_for_user = admin_add_finance_form.save(commit=False)
            finance_for_user.save()
            messages.success(request, f'finance added for {finance_for_user.user.username}')
            return redirect('homapp:all_finance_for_admin')


    context = {
        'admin_add_finance_form': admin_add_finance_form,
        'finance_for_user': finance_for_user,
    }
    return render(request, 'homapp/for_admin/admin_add_finance.html', context)


# For admin to edit any users finance
@login_required
@only_admin
def admin_edit_finance(request, pk):
    qs = get_object_or_404(Finance, id=pk)
    admin_edit_finance_form = AdminEditFinanceForm(instance=qs)
    if request.method == 'POST':
        admin_edit_finance_form = AdminEditFinanceForm(request.POST, instance=qs)
        if admin_edit_finance_form.is_valid():
            get_user = admin_edit_finance_form.save(commit=False)
            get_user.save()
            messages.success(request, f'finance for {get_user.user.username} was updated successfully')
            return redirect('homapp:all_finance_for_admin')

    context = {
        'qs': qs,
        'admin_edit_finance_form': admin_edit_finance_form,
    }
    return render(request, 'homapp/for_admin/admin_edit_finance.html', context)



# For admin to delete any user's finance
@login_required
@only_admin
def admin_delete_finance(request, pk):
    qs = get_object_or_404(Finance, id=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f'finance for {qs.user.username} was deleted successfully')
        return redirect('homapp:all_finance_for_admin')

    context = {
        'qs': qs,
    }
    return render(request, 'homapp/for_admin/admin_delete_finance.html', context)




# For admin users to see all Finance categories from all users
@login_required
@only_admin
def all_finance_categories_for_admin(request):
    count_with_data_selected = None

    all_finance_for_admin = Finance.objects.all()
    """ i am using values_list and adding flat=True and .distinct() so that i can get only the owners of each category and count them, 
    remember that a single user can have many categories created by only him/her, so i needed a way to count only those 
    categories creators only """
    total_finance_category_owner = FinanceCategory.objects.values_list('category_owner', flat=True).distinct()
    total_finance_categories = FinanceCategory.objects.all()
    total_deactivated_finance_categories = FinanceCategory.objects.filter(activate=False)

    # for my filter categories selection
    categories = FinanceCategory.objects.all()


    # getting the names from the form
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    activated = request.GET.get('activated')
    not_activated = request.GET.get('not_activated')
    search = request.GET.get('search')


    if start_date != '' and start_date != None:
        total_finance_categories = total_finance_categories.filter(date_created__gte=start_date)
        count_with_data_selected = total_finance_categories.filter(date_created__gte=start_date)

    

    if end_date != '' and end_date != None:
        total_finance_categories = total_finance_categories.filter(date_created__lt=end_date)
        count_with_data_selected = total_finance_categories.filter(date_created__lt=end_date)


    
    if search != '' and search != None: 
        total_finance_categories = total_finance_categories.filter(category_name__icontains=search)
        count_with_data_selected = total_finance_categories.filter(category_name__icontains=search)

        

    
    if activated == 'on':
        total_finance_categories = total_finance_categories.filter(activate=True)
        count_with_data_selected = total_finance_categories.filter(activate=True)
        
        
    elif not_activated == 'on':
        total_finance_categories = total_finance_categories.filter(activate=False)
        count_with_data_selected = total_finance_categories.filter(activate=False)

    context = {
        'all_finance_for_admin': all_finance_for_admin,
        'total_finance_category_owner': total_finance_category_owner,
        'total_finance_categories': total_finance_categories,
        'total_deactivated_finance_categories': total_deactivated_finance_categories,
        'count_with_data_selected': count_with_data_selected,
        'categories': categories,
    }
    return render(request, 'homapp/for_admin/all_finance_categories_for_admin.html', context)


# For admin to be able to add finance categories for any user
@login_required
@only_admin
def admin_add_finance_category(request):
    admin_add_finance_category_form = AdminAddFinanceCategoryForm()
    if request.method == 'POST':
        admin_add_finance_category_form = AdminAddFinanceCategoryForm(request.POST)
        if admin_add_finance_category_form.is_valid():
            get_user_username = admin_add_finance_category_form.save(commit=False)
            get_user_username.save()
            messages.success(request, f'{get_user_username.category_name} category was added successfully for {get_user_username.category_owner.username}')
            return redirect('homapp:all_finance_categories_for_admin')

    context = {
        'admin_add_finance_category_form': admin_add_finance_category_form,
    }
    return render(request, 'homapp/for_admin/admin_add_finance_category.html', context)



# For admin to be able to edit finance categories for any user
@login_required
@only_admin
def admin_edit_finance_category(request, pk):
    qs = get_object_or_404(FinanceCategory, id=pk)
    admin_edit_finance_category_form = AdminFinanceCategoryEditForm(instance=qs)
    if request.method == 'POST':
        admin_edit_finance_category_form = AdminFinanceCategoryEditForm(request.POST, instance=qs)
        if admin_edit_finance_category_form.is_valid():
            get_user_username = admin_edit_finance_category_form.save(commit=False)
            get_user_username.save()
            messages.success(request, f'{get_user_username.category_name} category was updated successfully for {get_user_username.category_owner.username}')
            return redirect('homapp:all_finance_categories_for_admin')

    context = {
        'qs': qs,
        'admin_edit_finance_category_form': admin_edit_finance_category_form,
    }
    return render(request, 'homapp/for_admin/admin_edit_finance_category.html', context)


# For admin to be able to delete finance category for any user
@login_required
@only_admin
def admin_delete_finance_category(request, pk):
    qs = get_object_or_404(FinanceCategory, id=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f'{qs.category_name} category was deleted successfully for {qs.category_owner.username}')
        return redirect('homapp:all_finance_categories_for_admin')
    
    context = {
        'qs': qs,
    }
    return render(request, 'homapp/for_admin/admin_delete_finance_category.html', context)


# For admin users to edit Task for any user
@login_required
@only_admin
def admin_edit_task(request, pk):
    qs = get_object_or_404(Task, id=pk)
    admin_edit_task_form = AdminEditTaskForm(instance=qs)
    if request.method == 'POST':
        admin_edit_task_form = AdminEditTaskForm(request.POST, instance=qs)
        if admin_edit_task_form.is_valid():
            get_user_username = admin_edit_task_form.save(commit=False)
            get_user_username.save()
            messages.success(request, f'task saved for {get_user_username.user.username}')
            return redirect('homapp:admin_list_and_add_task')

    context = {
        'qs': qs,
        'admin_edit_task_form': admin_edit_task_form,
    }
    return render(request, 'homapp/for_admin/admin_edit_task.html', context)


# For admin users to be able to delete task for any user
@login_required
@only_admin
def admin_delete_task(request, pk):
    qs = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f'Task for {qs.user.username} was deleted successfully')
        return redirect('homapp:admin_list_and_add_task')
    context = {
        'qs': qs,
    }
    return render(request, 'homapp/for_admin/admin_delete_task.html', context)




# For admin to add wear for any user
@login_required
@only_admin
def admin_add_wear(request):
    admin_add_wear_form = AdminAddWearForm()  
    if request.method == 'POST':
        admin_add_wear_form = AdminAddWearForm(request.POST, request.FILES)
        if admin_add_wear_form.is_valid():
            get_username_for_wear = admin_add_wear_form.save(commit=False)
            get_username_for_wear.save()
            messages.success(request, f'wear added for {get_username_for_wear.user.username}')
            return redirect('homapp:all_wears_for_admin')

    

    context = {
        'admin_add_wear_form': admin_add_wear_form,
    }
    return render(request, 'homapp/for_admin/admin_add_wear.html', context)



# For admin to add task for any user
@login_required 
@only_admin
def admin_list_and_add_task(request):
    count_task_filtered = None
    selected_task_category = None
    
    all_task = Task.objects.filter(activate=True).order_by( 'complete', 'due')

    # This is to count all users that create a task
    all_users_that_create_task = Task.objects.values_list('user', flat=True).distinct()

    # This particular database query is for pagination purposes only...
    # hmm = Task.objects.filter(user_id=request.user.id, activate=True).order_by('complete', 'due')

    # for pagination logic
    # paginator = Paginator(all_task, 10)
    # page = request.GET.get('page', 1)

    # try:
    #     all_task = paginator.page(page)
    # except PageNotAnInteger:
    #     all_task = paginator.page(1)
    # except EmptyPage:
    #     all_task = paginator.page(paginator.num_pages)



    admin_add_task_form = AdminAddTaskForm()
    if request.method == 'POST':
        admin_add_task_form = AdminAddTaskForm(request.POST)
        if admin_add_task_form.is_valid():
            get_task_user_username = admin_add_task_form.save(commit=False)
            get_task_user_username.save()
            admin_add_task_form = AdminAddTaskForm()
            messages.success(request, f'Task added successfully {get_task_user_username.user.username}'.title())
            return redirect('homapp:admin_list_and_add_task')
    

    # counting all tasks 
    all_task_count = Task.objects.filter()

    # Counting all uncompleted Tasks
    uncompleted_tasks = Task.objects.filter(complete=False).count()

    # counting all completed tasks
    completed_tasks = Task.objects.filter(complete=True).count()

    # All deactivated tasks
    deactivated_tasks = Task.objects.filter(activate=False).count()

    # Task categories
    task_categories = TaskCategory.objects.filter(activate=True)

    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    completed = request.GET.get('completed')
    not_completed = request.GET.get('not_completed')
    search = request.GET.get('search')

    if category != '' and category != None and category != 'Choose...':
        all_task = all_task.filter(category_id=category)
        count_task_filtered = all_task.filter(category_id=category)
        selected_task_category = get_object_or_404(TaskCategory, id=category)
    
    if start_date != '' and start_date != None:
        all_task = all_task.filter(date_created__gte=start_date)
        count_task_filtered = all_task.filter(date_created__gte=start_date)
        
    
    if end_date != '' and end_date != None:
        all_task = all_task.filter(date_created__lt=end_date)
        count_task_filtered = all_task.filter(date_created__lt=end_date)
    
    if search != '' and search != None: 
        all_task = all_task.filter(name__icontains=search)
        count_task_filtered = all_task.filter(name__icontains=search)
    
    if completed == 'on':
        all_task = all_task.filter(complete=True)
        count_task_filtered = all_task.filter(complete=True)
       

    elif not_completed == 'on':
        all_task = all_task.filter(complete=False)
        count_task_filtered = all_task.filter(complete=False)
        

   



    context = {
        'all_task': all_task,
        'admin_add_task_form': admin_add_task_form,
        'all_task_count': all_task_count,
        'uncompleted_tasks': uncompleted_tasks,
        'completed_tasks': completed_tasks,
        'deactivated_tasks': deactivated_tasks,
        'task_categories': task_categories,
        'count_task_filtered': count_task_filtered,
        'all_users_that_create_task': all_users_that_create_task,
    }
    return render(request, 'homapp/for_admin/admin_list_and_add_task.html', context)



# For admin to see all task categories from all users
@login_required
@only_admin
def all_task_categories_for_admin(request):
    count_task_filtered = None
    selected_task_category = None
    
    all_task_category = TaskCategory.objects.all().order_by('-date_created')
    deactivated_task_categories = TaskCategory.objects.filter(activate=False).order_by('-date_created').count()

    # This is to count all users that create task category, remember a single user can create and have many task so i am going to use values_list for this
    users_that_create_task_categories = TaskCategory.objects.values_list('user', flat=True).distinct()
    

    add_task_category_form = TaskCategoryForm()

    if request.method == 'POST':
        add_task_category_form = TaskCategoryForm(request.POST)
        if add_task_category_form.is_valid():
            add_user = add_task_category_form.save(commit=False)
            add_user.save()
            add_task_category_form = TaskCategoryForm()
            messages.success(request, f'Task category was created successfully for {add_user.user.username}'.title())
            return redirect('homapp:all_task_categories_for_admin')
    

    

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search = request.GET.get('search')
    activated = request.GET.get('activated')
    not_activated = request.GET.get('not_activated')


    if start_date != '' and start_date != None:
        all_task_category = all_task_category.filter(date_created__gte=start_date)
        count_task_filtered = all_task_category.filter(date_created__gte=start_date)
        
    
    if end_date != '' and end_date != None:
        all_task_category = all_task_category.filter(date_created__lt=end_date)
        count_task_filtered = all_task_category.filter(date_created__lt=end_date)
    
    if search != '' and search != None: 
        all_task_category = all_task_category.filter(name__icontains=search)
        count_task_filtered = all_task_category.filter(name__icontains=search)

    if activated == 'on':
        all_task_category = all_task_category.filter(activate=True)
        count_with_data_selected = all_task_category.filter(activate=True)
        
        
    elif not_activated == 'on':
        all_task_category = all_task_category.filter(activate=False)
        count_with_data_selected = all_task_category.filter(activate=False)
    
    # last added task category
    last_added_task_category = TaskCategory.objects.filter(activate=True).order_by('-date_created')[:1]


    
    

    context = {
        'all_task_category': all_task_category,
        'add_task_category_form': add_task_category_form,
        'deactivated_task_categories': deactivated_task_categories,
        'count_task_filtered': count_task_filtered,
        'last_added_task_category': last_added_task_category,
        'users_that_create_task_categories': users_that_create_task_categories,
    }
    return render(request, 'homapp/for_admin/all_task_categories_for_admin.html', context)




# For admin to edit task categories for any all user selected
@login_required
@only_admin
def admin_edit_task_category(request, pk):
    count_task_filtered = None
    selected_task_category = None
    
    all_task_category = TaskCategory.objects.all().order_by('-date_created')
    deactivated_task_categories = TaskCategory.objects.filter(activate=False).order_by('-date_created').count()

    # This is to count all users that create task category, remember a single user can create and have many task so i am going to use values_list for this
    users_that_create_task_categories = TaskCategory.objects.values_list('user', flat=True).distinct()
    
    qs = get_object_or_404(TaskCategory, id=pk)
    admin_edit_task_category_form = AdminEditTaskCategoryForm(instance=qs)

    if request.method == 'POST':
        admin_edit_task_category_form = AdminEditTaskCategoryForm(request.POST, instance=qs)
        if admin_edit_task_category_form.is_valid():
            get_name = admin_edit_task_category_form.save(commit=False)
            get_name.save()
            messages.success(request, f'task category updated successfully for {get_name.user.username}')
            return redirect('homapp:all_task_categories_for_admin')
    

    

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search = request.GET.get('search')
    activated = request.GET.get('activated')
    not_activated = request.GET.get('not_activated')


    if start_date != '' and start_date != None:
        all_task_category = all_task_category.filter(date_created__gte=start_date)
        count_task_filtered = all_task_category.filter(date_created__gte=start_date)
        
    
    if end_date != '' and end_date != None:
        all_task_category = all_task_category.filter(date_created__lt=end_date)
        count_task_filtered = all_task_category.filter(date_created__lt=end_date)
    
    if search != '' and search != None: 
        all_task_category = all_task_category.filter(name__icontains=search)
        count_task_filtered = all_task_category.filter(name__icontains=search)

    if activated == 'on':
        all_task_category = all_task_category.filter(activate=True)
        count_with_data_selected = all_task_category.filter(activate=True)
        
        
    elif not_activated == 'on':
        all_task_category = all_task_category.filter(activate=False)
        count_with_data_selected = all_task_category.filter(activate=False)
    
    # last added task category
    last_added_task_category = TaskCategory.objects.filter(activate=True).order_by('-date_created')[:1]


    
    

    context = {
        'all_task_category': all_task_category,
        'admin_edit_task_category_form': admin_edit_task_category_form,
        'qs': qs,
        'deactivated_task_categories': deactivated_task_categories,
        'count_task_filtered': count_task_filtered,
        'last_added_task_category': last_added_task_category,
        'users_that_create_task_categories': users_that_create_task_categories,
    }
    return render(request, 'homapp/for_admin/admin_edit_task_categories.html', context)


# Admin delete task categories on any selected user
@login_required
@only_admin
def admin_delete_task_category(request, pk):
    qs = get_object_or_404(TaskCategory, id=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f' Task category was deleted successfully for {qs.user.username}')
        return redirect('homapp:all_task_categories_for_admin')
    context = {
        'qs': qs,

    }
    return render(request, 'homapp/for_admin/admin_delete_task_category.html', context)


