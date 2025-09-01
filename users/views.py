from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator



from django.contrib.auth.models import User, Group

from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch


# Create your views here.

def home(request):
    return render(request, 'home.html')


def sign_up(request):
    form = CustomRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()  
        messages.success(request, "Please check your email to activate your account.")
        return redirect('sign-in')
    return render(request, 'registration/register.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid credentials.")
        else:
            if not user.is_active:
                messages.error(request, "Please activate your account from the email we sent.")
            else:
                login(request, user)
                return redirect('post-login-redirect')  
    return render(request, 'registration/login.html')

def sign_out(request):
    logout(request)
    return redirect('sign-in')
    
def activate_user(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('sign-in')
    except User.DoesNotExist:
        return HttpResponse('User doesnt exist')
    
def admin_dashboard(request):
    users=User.objects.all()
    return render(request,'admin/dashboard.html')


# @user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  
            user.groups.add(role)
            messages.success(request, f"User {
                             user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})


# @user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {
                             group.name} has been created successfully")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})


# @user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})

def post_login_redirect(request):
    u = request.user
    if not u.is_authenticated:
        return redirect('sign-in')
    if u.is_superuser or u.groups.filter(name='Admin').exists():
        return redirect('admin-dashboard')
    if u.groups.filter(name='Organizer').exists():
        return redirect('organizer-dashboard')
    return redirect('participant-dashboard')

