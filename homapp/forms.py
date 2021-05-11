from crispy_forms.helper import FormHelper  
from django import forms  
from homapp.models import Wear, WearCategory, Finance, FinanceCategory, Task, TaskCategory
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class WearRegisterForm(forms.ModelForm):
    class Meta:
        model = Wear  
        fields = ('name', 'description', 'category', 
                  'amount', 'photo',  
                  'bought_from', 'activate', 'expenses')

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 3
    }))

    # This will query all categories that belong to this particular user and push them in this form field (category)
    def __init__(self, user, *args, **kwargs):
        super(WearRegisterForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = WearCategory.objects.filter(category_owner_id=user.id)


    


    
  

class WearEditForm(forms.ModelForm):
    class Meta:
        model = Wear    
        fields = ('name', 'description', 'category', 
                  'amount', 'photo',  
                  'bought_from', 'activate', 'expenses')
    
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 3
    }))


    # This will query all categories that belong to this particular user and push them in this form field (category)
    def __init__(self, user, *args, **kwargs):
        super(WearEditForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = WearCategory.objects.filter(category_owner_id=user.id)



class CatSelectForm(forms.ModelForm):
    class Meta:
        model = Wear 
        fields = '__all__'
        exclude = ['user', 'name', 'photo', 'description', 'date_created',
                    'date_updated', 'amount', 'date_bought', 'bought_from',  'activate']
    
    
    
    def __init__(self, *args, **kwargs):
        super(CatSelectForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = False


# class DateSelectForm(forms.ModelForm):
#     class Meta:
#         model = Wear 
#         fields = '__all__'
#         exclude = ['user', 'name', 'photo', 'description', 'date_created',
#                     'date_updated', 'amount', 'date_bought', 'bought_from', 'activate']


#     start_date = forms.DateTimeField(required=False)
#     end_date = forms.DateTimeField(required=False)
   
    

    
    
    # def __init__(self, *args, **kwargs):
    #     super(CatSelectForm, self).__init__(*args, **kwargs)
    #     self.fields['date_created'].label = False


    


class FinCatSelectForm(forms.ModelForm):
    class Meta:
        model = Finance
        fields = '__all__'
        exclude = ['user', 'title', 'description', 'amount', 'date_created',
                    'date_updated', 'activate', 'expenses']
    
    
    
    def __init__(self, *args, **kwargs):
        super(FinCatSelectForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = False

      # This will query all categories that belong to this particular user and push them in this form field (category)
    def __init__(self, user, *args, **kwargs):
        super(FinCatSelectForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = FinanceCategory.objects.filter(category_owner_id=user.id)





class AddCategoryForm(forms.ModelForm):
    class Meta: 
        model = WearCategory  
        fields = ('category_name', 'activate')
    
    category_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Add name",
        
    }))

class CatEditForm(forms.ModelForm):
    class Meta:
        model = WearCategory  
        fields = ('category_name', 'activate')



class FinanceAddForm(forms.ModelForm):
    class Meta:
        model = Finance  
        fields = ('title', 'description', 'category', 
                  'amount', 'activate', 'expenses', 'photo')

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 3
    }))

    # This will query all categories that belong to this particular user and push them in this form field (category)
    def __init__(self, user, *args, **kwargs):
        super(FinanceAddForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = FinanceCategory.objects.filter(category_owner_id=user.id)




class EditFinanceForm(forms.ModelForm):
    class Meta:
        model = Finance  
        fields = ('title', 'description', 'category', 
                  'amount', 'activate', 'expenses', 'photo')
                  
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 3
    }))

    # This will query all categories that belong to this particular user and push them in this form field (category)
    def __init__(self, user, *args, **kwargs):
        super(EditFinanceForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = FinanceCategory.objects.filter(category_owner_id=user.id)




class AddFinanceCategoryForm(forms.ModelForm):
    class Meta: 
        model = FinanceCategory 
        fields = ('category_name', 'activate')
    
    category_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Add category name",
        
    }))

class FinanceCatEditForm(forms.ModelForm):
    class Meta:
        model = FinanceCategory  
        fields = ('category_name', 'activate')


class FinanceDeactivatedCatForm(forms.ModelForm):
    class Meta:
        model = FinanceCategory
        fields = ('category_name', 'activate')


# form for editing finance deactivated page
class EditFinanceDectForm(forms.ModelForm):
    class Meta:
        model = Finance  
        fields = ('title', 'description', 'category', 
                  'amount', 'activate', 'expenses')
                  
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 3
    }))

    # This will query all categories that belong to this particular user and push them in this form field (category)
    def __init__(self, user, *args, **kwargs):
        super(EditFinanceDectForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = FinanceCategory.objects.filter(category_owner_id=user.id)

    


class DateTimeInput(forms.DateTimeInput):
    # This is the datetime calendar am using from HTML 5
    input_type = 'datetime-local'
    # not in use at the moment




class TodoForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'due', 'category', 'complete', 'activate')
        # widgets = {
        #     'due': DateTimeInput()
           
        # }
    
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 2,
    }))

    due = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    # This will query all categories that belong to this particular user and push them in this form field (category)
    def __init__(self, user, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = TaskCategory.objects.filter(user_id=user.id)

   
class UpdateTodoForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'due', 'category', 'complete', 'activate')

        # widgets = {
        #     'due': DateTimeInput()
    
        # }
    
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 2
    }))

    due = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    # This will query all categories that belong to this particular user and push them in this form field (category)
    def __init__(self, user, *args, **kwargs):
        super(UpdateTodoForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = TaskCategory.objects.filter(user_id=user.id)

    

class TaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory 
        fields = ('user', 'name', 'activate')

        

class UpdateTaskCategoryForm(forms.ModelForm):
    class Meta: 
        model = TaskCategory  
        fields = ('name', 'activate')

    








# All admin form here 

# For admin to add finance for any user
class AdminAddFinanceForm(forms.ModelForm):
    class Meta:
        model = Finance  
        fields = ('user', 'title', 'description', 'category', 
                  'amount', 'activate', 'expenses', 'photo')

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 3
    }))

    # This will query all categories that belong to this particular user and push them in this form field (category)
    # def __init__(self, user, *args, **kwargs):
    #     super(FinanceAddForm, self).__init__(*args, **kwargs)
    #     self.fields['category'].queryset = FinanceCategory.objects.filter(category_owner_id=user.id)


# For admin to edit finance for any user
class AdminEditFinanceForm(forms.ModelForm):
    class Meta:
        model = Finance  
        fields = ('user', 'title', 'description', 'category', 
                  'amount', 'activate', 'expenses', 'photo')

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 3
    }))



# Form For admin to use and add finance category
class AdminAddFinanceCategoryForm(forms.ModelForm):
    class Meta: 
        model = FinanceCategory 
        fields = ('category_owner', 'category_name', 'activate')
    
    category_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Add category name",
        
    }))


# Form for admin to use and edit finance category
class AdminFinanceCategoryEditForm(forms.ModelForm):
    class Meta:
        model = FinanceCategory  
        fields = ('category_owner', 'category_name', 'activate')





# For admin to add wear for any user
class AdminAddWearForm(forms.ModelForm):
    class Meta:
        model = Wear  
        fields = ('user', 'name', 'description', 'category', 
                  'amount', 'photo',  
                  'bought_from', 'activate', 'expenses')

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 3
    }))



# For admin to edit wear for any user
class AdminEditWearForm(forms.ModelForm):
    class Meta:
        model = Wear  
        fields = ('user', 'name', 'description', 'category', 
                  'amount', 'photo',  
                  'bought_from', 'activate', 'expenses')

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 3
    }))



# Admin add wear categories
class AdminAddWearCategoryForm(forms.ModelForm):
    class Meta: 
        model = WearCategory  
        fields = ('category_owner', 'category_name', 'activate')
    
    category_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Add name",
        
    }))

# Admin edit wear category form for any user
class AdminEditWearCategoryForm(forms.ModelForm):
    class Meta:
        model = WearCategory  
        fields = ('category_owner', 'category_name', 'activate')





# For admin to add Task for any user
class AdminAddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('user', 'name', 'description', 'due', 'category', 'complete', 'activate')
        # widgets = {
        #     'due': DateTimeInput()
           
        # }
    
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 2,
    }))

    due = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )



# For only admin to use and edit task for any user
class AdminEditTaskForm(forms.ModelForm): 
    class Meta:
        model = Task
        fields = ('user', 'name', 'description', 'due', 'category', 'complete', 'activate')

        # widgets = {
        #     'due': DateTimeInput()
    
        # }
    
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some description",
        "rows": 2
    }))

    due = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )



# Admin edit task category form
# For only admin to use and edit task for any user
class AdminEditTaskCategoryForm(forms.ModelForm): 
    class Meta:
        model = TaskCategory
        fields = ('user', 'name', 'activate')


