from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from tasks.models import Task, Comment, Theme
from tasks.forms import TaskForm, TaskFilterForm
from tasks.mixins import UserIsOwnerMixins


# --- TASK LOGIC ---

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


# --- THEME SYSTEM ---

class ThemeEditorView(LoginRequiredMixin, TemplateView):
    template_name = 'editor.html'

class ThemeWorkshopView(LoginRequiredMixin, ListView):
    model = Theme
    template_name = 'workshop.html'
    context_object_name = 'themes'
