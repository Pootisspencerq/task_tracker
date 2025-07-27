from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks:task-list')


    context = {
        'form': form
    }

    return render(request, template_name = 'tasks/register.html', context=context)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks:task-list')

    context = {
        'form': form
    }

    return render(request, template_name='tasks/login.html', context=context)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('login-page')