from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Task, Category
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def index(request):
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'tasks/index.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        comments = request.POST.get('comments')
        deadline = request.POST.get('deadline')
        category_id = request.POST.get('category')

        category = Category.objects.get(id=category_id) if category_id else None

        if title:
            Task.objects.create(
                owner=request.user,
                title=title,
                description=description,
                comments=comments,
                deadline=deadline,
                category=category
            )
            return redirect('index')
    categories = Category.objects.all()
    return render(request, 'tasks/create_task.html', {'categories': categories})