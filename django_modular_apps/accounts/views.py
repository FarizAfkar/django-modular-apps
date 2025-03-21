from functools import wraps
from django.shortcuts import render, redirect
from accounts.forms import RegisterForm, LogInForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_excluded(redirect_to):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator

@login_excluded('modules:home')
def url_dispatcher(request):
    return redirect('accounts:login')

@login_excluded('modules:home')
def register_view(request):
    # Set Register
    next = request.GET.get('next')
    form = RegisterForm(request.POST or None)

    # Request Post
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            if next:
                messages.success(request, f'You are now logged in as {username}.')
                return redirect(next)

            messages.success(request, f'You are now logged in as {username}.')
            return redirect('modules:home')

    # Render Context to HTML
    context = {
        'form' : form
    }

    return render(request, 'accounts/register.html', context)


@login_excluded('modules:home')
def login_view(request):
    # Set Login
    next = request.GET.get('next')
    form = LogInForm(request.POST or None)

    # Request Post
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if next:
                    messages.success(request, f'You are now logged in as {username}.')
                    return redirect(next)
                messages.success(request, f'You are now logged in as {username}.')
                return redirect('modules:home')
            else:
                messages.error(request, 'Invalid Username or Password')
        else:
            messages.error(request, 'Invalid Username or Password')

    # Render Context to HTML
    context = {
        'form' : form
    }

    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('url_dispatcher')
