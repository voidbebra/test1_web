from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# git test
from .forms import CreateUserForm


def maine(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


@login_required(login_url='login')
def get_user_list(request):
    from django.contrib.auth.models import User

    users = User.objects.all()
    context = {'users': users}

    return render(request, 'main/users_list.html', context)


def dj_register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')

    context = {
        'form': form,
        'form_name': 'Register Account',
        'info_text': 'Already have an account?',
        'info_url': 'login',
        'info_btn_text': 'Sign in'
    }
    return render(request, 'main/register.html', context)


def dj_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or password is incorrect')

    context = {
        'form_name': 'Login',
        'info_text': 'Don\'t have an account?',
        'info_url': 'register',
        'info_btn_text': 'Sign up'
    }
    return render(request, 'main/login.html', context)


def dj_logout(request):
    logout(request)
    return redirect('home')
