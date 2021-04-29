from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, AdminPasswordChangeForm  # For default django auth forms
from django import forms 
from .models import Profile  


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Repeat Password"
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "First Name"
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Last Name"
    }))

    class Meta:
        model = User 
        fields = ('username', 'email', 'first_name', 'last_name')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords don\'t match'.title())
        return cd['password2']



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
        }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password" 
        }))
        



class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User 
        fields = ('old_password', 'new_password1', 'new_password2')
    
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Old Password"}))
    
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "New Password"}))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Confirm New Password"}))


# This form is to allow users change password without having to put in their old password
class UserSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User 
        fields = ('new_password1', 'new_password2')
    

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "New Password"}))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Confirm New Password"}))




# This form is to allow admin change users password without having to put in their old password
class AdminSetPasswordForm(AdminPasswordChangeForm):
    class Meta:
        model = User 
        fields = ('password1', 'password2')
    

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "New Password"}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Confirm New Password"}))




class CustomizePasswordResetForm(PasswordResetForm):
    class Meta:
        model = User 
        fields = ('email')

    email = forms.EmailField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))


# class CustomizePasswordResetDoneForm(SetPasswordForm):
#     class Meta:
#         model = User 
#         fields = ('new_password1', 'new_password2')

#     news_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
#         "class": "form-control",
#         "type": "password",
#         "placeholder": "Password" }))

#     news_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
#         "class": "form-control",
#         "type": "password",CustomizePasswordResetCompleteView
#         "placeholder": "Confirm Password" }))



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('first_name', 'last_name', 'email')




class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile  
        fields = ('profile_pic', 'educational_background', 'occupation', 
                  'home_address', 'phone_no', 'sex', 'marital_status', 'notes',
                    )
      
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some notes, this could be about yourself or anything.......",
        "rows": 2,
    }))

    
    # educational_background = forms.CharField(required=False, widget=forms.TextInput(attrs={
    #     "class": "form-control",
    #     "placeholder": "Educational Background"
    # }))

    # occupation = forms.CharField(widget=forms.TextInput(attrs={
    #     "class": "form-control",
    #     "placeholder": "Occupation"
    # }))

    # home_address = forms.CharField(widget=forms.TextInput(attrs={
    #     "class": "form-control",
    #     "placeholder": "Home Address"
    # }))

    # phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={
    #     "class": "form-control",
    #     "placeholder": "Your phone number"
    # }))

    # SEX = [('Male', 'Male'),
    #     ('Female', 'Female')
    # ]

    # sex = forms.ChoiceField(choices=SEX, widget=forms.Select(attrs={
    #     "class": "form-control"
    # }))

    # profile_pic = forms.FileField(widget=forms.FileInput(attrs={
    #     "class": "custom-file-input"
        
    # }))



class AdminEditUserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active')




class AdminEditUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  
        fields = ('profile_pic', 'educational_background', 'occupation', 
                  'home_address', 'phone_no', 'sex', 'marital_status', 'notes',
                    )
      
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Add some notes, this could be about yourself or anything.......",
        "rows": 2,
    }))