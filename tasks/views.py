from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from tasks.models import Task, Theme, Note
from tasks.forms import TaskForm, TaskFilterForm, ThemeForm
from tasks.mixins import UserIsOwnerMixins

# --- TASKS ---
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(creator=self.request.user)
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixins, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update_form.html'
    success_url = reverse_lazy('tasks:task-list')

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixins, DeleteView):
    model = Task
    template_name = 'tasks/task_delete_confirmation.html'
    success_url = reverse_lazy('tasks:task-list')

class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixins, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = 'done'
        task.save()
        return HttpResponseRedirect(reverse_lazy('tasks:task-list'))

    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=task_id)


# --- THEMES ---
class ThemeWorkshopView(LoginRequiredMixin, ListView):
    model = Theme
    template_name = 'theme/theme_list.html'
    context_object_name = 'themes'

class ThemeEditorView(LoginRequiredMixin, CreateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'theme/theme_form.html'
    success_url = reverse_lazy('tasks:workshop')   # після створення повертає у список

class ThemeUpdateView(LoginRequiredMixin, UpdateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'theme/theme_form.html'
    success_url = reverse_lazy('tasks:workshop')   # після редагування повертає у список

class ThemeDeleteView(LoginRequiredMixin, DeleteView):
    model = Theme
    template_name = 'theme/theme_confirm_delete.html'
    success_url = reverse_lazy('tasks:workshop')   # після видалення повертає у список


# --- NOTES ---
class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'content']  # або свої поля моделі
    template_name = 'tasks/note_create.html'
    success_url = reverse_lazy('tasks:note-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'tasks/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
