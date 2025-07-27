from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from tasks import models
from tasks.forms import TaskForm, TaskFilterForm, NoteForm
from tasks.mixins import UserIsOwnerMixins
from .forms import NoteForm

class TaskListView(LoginRequiredMixin, ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.filter(creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_form'] = NoteForm()
        context['notes'] = self.object.notes.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.task = self.object
            note.author = request.user
            note.save()
            return HttpResponseRedirect(self.request.path_info)
        context = self.get_context_data(note_form=form)
        return self.render_to_response(context)



class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixins, UpdateView):
    model = models.Task
    form_class = TaskForm
    template_name = 'tasks/task_update_form.html'
    success_url = reverse_lazy('tasks:task-list')


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixins, DeleteView):
    model = models.Task
    success_url = reverse_lazy('tasks:task-list')
    template_name = 'tasks/task_delete_confirmation.html'


class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixins, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = 'done'
        task.save()
        return HttpResponseRedirect(reverse_lazy('tasks:task-list'))

    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(models.Task, pk=task_id)


# ✅ Додано створення Note з image
class NoteCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task_id = self.kwargs.get('pk')
        task = get_object_or_404(models.Task, pk=task_id, creator=request.user)
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.task = task
            note.user = request.user
            note.save()
        return HttpResponseRedirect(task.get_absolute_url())
