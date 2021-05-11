from django.shortcuts import render, redirect, get_object_or_404 
from .forms import UserEditForm, UserSetPasswordForm, AdminAddUserForm,  AdminSetPasswordForm, AdminEditUserForm, AdminEditUserProfileForm, ProfileEditForm, UserRegistrationForm, LoginForm, ChangePasswordForm, CustomizePasswordResetForm
from .models import Profile 
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, AdminPasswordChangeForm # For default auth Forms
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView # For default auth Views
from django.urls import reverse_lazy  # For auth views successful reverse page
from django.contrib.auth.models import User
from homapp_project.decorators import only_admin, unauthorized_user
from homapp.models import Wear, Finance


@unauthorized_user
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, f"account for {new_user.username} has been created successfully".title())
            return redirect('login')    
        else:
            messages.error(request, 'credentials incorrect or password mismatch')    
    else:
        user_form = UserRegistrationForm()
    context = {
        'user_form': user_form,
    }
    return render(request, 'account/register.html', context)

@unauthorized_user
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'welcome {user.username}')
                    return redirect('homapp:wears_list')
        messages.error(request, 'invalid username or password, username do not match with password registered'.title())
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

class CustomizePasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """ Here, i subclass the default django class base view called PasswordChangeView and i used that to customize
    and program my own view called CustomizePasswordChangeView """
    form_class = ChangePasswordForm
    template_name = 'account/passwords_change.html'
    success_url = reverse_lazy('login')
    success_message = 'Your password was change successfully'


class CustomizePasswordResetView(PasswordResetView):
    form_class = CustomizePasswordResetForm
    template_name = 'account/passwords_reset.html'
    success_url = reverse_lazy('passwords_reset_done')

class CustomizePasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/passwords_reset_done.html'
    

# class CustomizePasswordResetCompleteView(PasswordResetCompleteView):
#     form_class = CustomizePasswordResetDoneForm    
#     template_name = 'account/passwords_reset_complete.html'
#     success_url = reverse_lazy('')
    
# This view is to allow users set their password without giving the old one
@login_required
def password_set(request):
    password_set_form = UserSetPasswordForm(user=request.user)
    if request.method == 'POST':
        password_set_form = UserSetPasswordForm(user=request.user, data=request.POST)
        if password_set_form.is_valid():
            password_set_form.save()
            update_session_auth_hash(request, password_set_form.user)
            messages.success(request, 'your password has been changed successfully')
            return redirect('logout')

    context = {
        'password_set_form': password_set_form,
    }
    return render(request, 'account/password_set.html', context)



# This view is to allow admin change any user's password
@login_required
@only_admin
def admin_change_user_password(request, pk):
    qs = get_object_or_404(User, id=pk)
    adminChangeUserPasswordForm = AdminSetPasswordForm(user=qs)
    if request.method == 'POST':
        adminChangeUserPasswordForm = AdminSetPasswordForm(user=qs, data=request.POST)
        if adminChangeUserPasswordForm.is_valid():
            new = adminChangeUserPasswordForm.save(commit=False)
            new.save()
            update_session_auth_hash(request, adminChangeUserPasswordForm.user)
            messages.success(request, f'password for {new.username} was change successfully')
            return redirect('all_users')

    context = {
        'qs': qs,
        'adminChangeUserPasswordForm': adminChangeUserPasswordForm,
    }
    return render(request, 'account/admin_change_user_password.html', context)


def logout_user(request):
    logout(request)  
    messages.success(request, 'logout successfully')                
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'account/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'your profile has been updated successfully'.title())
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit_profile.html', {"user_form": user_form, "profile_form": profile_form})






# THIS SECTION IS FOR ADMIN ONLY
@login_required
@only_admin
def admin_register_user(request):
    admin_add_user_form = AdminAddUserForm()
    if request.method == 'POST':
        admin_add_user_form = AdminAddUserForm(data=request.POST)
        if admin_add_user_form.is_valid():
            new_user_added = admin_add_user_form.save(commit=False)
            new_user_added.set_password(admin_add_user_form.cleaned_data['password'])
            new_user_added.save()
            messages.success(request, f'{new_user_added.username} was created successfully')
            return redirect('all_users')
        else:
            messages.error(request, 'credentials incorrect, confirm that the two password match')
    context = {
        'admin_add_user_form': admin_add_user_form,
    }
    return render(request, 'account/admin_register_user.html', context)


# List all users for admin only
@login_required
@only_admin
def all_users(request):          

    count_users_data_selected = None
    
    all_users = User.objects.all().order_by('-date_joined')

    # to count all admin users
    admin_users = User.objects.filter(is_staff=True, is_superuser=True).count()

    # to count all normal users
    normal_users = User.objects.filter(is_staff=False, is_superuser=False).count()

    # to count all non active users
    non_active_userss = User.objects.filter(is_active=False).count()

    # count all active users
    active_userss = User.objects.filter(is_active=True).count()


    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    active_users = request.GET.get('active_users')
    non_active_users = request.GET.get('non_active_users')
    search = request.GET.get('search')


    if start_date != '' and start_date != None:
        all_users = all_users.filter(date_joined__gte=start_date)
        count_users_data_selected = all_users.filter(date_joined__gte=start_date)

        

    if end_date != '' and end_date != None:
        all_users = all_users.filter(date_joined__lt=end_date)
        count_users_data_selected = all_users.filter(date_joined__lt=end_date)



    
    if search != '' and search != None: 
        all_users = all_users.filter(username__icontains=search)
        count_users_data_selected = all_users.filter(username__icontains=search)


    if active_users == 'on':
        all_users = all_users.filter(is_active=True)
        count_users_data_selected = all_users.filter(is_active=True)
        
        
    elif non_active_users == 'on':
        all_users = all_users.filter(is_active=False)
        count_users_data_selected = all_users.filter(is_active=False)


        

    context = {
        'all_users': all_users,
        'admin_users': admin_users,
        'normal_users': normal_users,
        'non_active_userss': non_active_userss,
        'active_userss': active_userss,
        'count_users_data_selected': count_users_data_selected,
    }
    return render(request, 'account/all_users.html', context)



# Edit users by admin only
@login_required
@only_admin
def edit_user(request, pk):
    qs = get_object_or_404(User, id=pk)
    admin_edit_user_form = AdminEditUserForm(instance=qs)
    admin_edit_user_profile_form = AdminEditUserProfileForm(instance=qs.profile)

    # processing the form
    if request.method == 'POST':
        admin_edit_user_form = AdminEditUserForm(instance=qs, data=request.POST)
        admin_edit_user_profile_form = AdminEditUserProfileForm(instance=qs.profile, data=request.POST, files=request.FILES)
        if admin_edit_user_form.is_valid() and admin_edit_user_profile_form.is_valid():
            get_username = admin_edit_user_form.save(commit=False)
            get_username.save()
            admin_edit_user_profile_form.save()
            messages.success(request, f'{get_username.username} account was updated successfully')
            return redirect('all_users')
            
    context = {
        'admin_edit_user_form': admin_edit_user_form,
        'admin_edit_user_profile_form': admin_edit_user_profile_form,
        'qs': qs,
    }
    return render(request, 'account/edit_user.html', context)


# delete a user  
@login_required
@only_admin  
def delete_user(request, pk): 
    qs = get_object_or_404(User, id=pk)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, f'{qs.username} account was deleted successfully')
        return redirect('all_users')
    context = {
        'qs': qs,
    }
    return render(request, 'account/delete_user.html', context)


# for detail of each user
@login_required
@only_admin
def detail_for_admin(request, pk):
    qs = get_object_or_404(User, id=pk)
    all_wears = Wear.objects.filter(user_id=qs.id)


    context = {
        'qs': qs,
        'all_wears': all_wears,

    }
    return render(request, 'account/detail_for_admin.html', context)

@login_required
@only_admin  
def user_wear(request, pk):
    qs = get_object_or_404(User, id=pk)
    all_wears = Wear.objects.filter(user_id=qs.id)

    context = {
        'all_wears': all_wears, 
        'qs': qs,
    }
    return render(request, 'account/user_wear.html', context)

@login_required
@only_admin
def all_wears_from_all_users(request):
    all_wears = Wear.objects.all()
    
    context = {
        'all_wears': all_wears,
    }
    return render(request, 'account/all_wears_from_all_users.html', context)