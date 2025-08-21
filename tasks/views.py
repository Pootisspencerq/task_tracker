from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from tasks.models import Task, Theme, Note
from tasks.forms import TaskForm, TaskFilterForm, ThemeForm
from tasks.mixins import UserIsOwnerMixins


# --- THEME SWITCH ---
def set_active_theme(request, theme_id):
    if request.user.is_authenticated:
        theme = get_object_or_404(Theme, id=theme_id, user=request.user)
        # всі інші неактивні
        Theme.objects.filter(user=request.user).update(is_active=False)
        # цю активуємо
        theme.is_active = True
        theme.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


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
def theme_create(request):
    if request.method == "POST":
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = form.save(commit=False)
            theme.user = request.user   # 🔑 Прив’язуємо автора
            theme.save()
            return redirect("themes:theme_list")
    else:
        form = ThemeForm()
    return render(request, "themes/theme_form.html", {"form": form})


class ThemeWorkshopView(LoginRequiredMixin, ListView):
    model = Theme
    template_name = 'themes/theme_list.html'
    context_object_name = 'themes'

    def get_queryset(self):
        return Theme.objects.filter(user=self.request.user)


class ThemeEditorView(LoginRequiredMixin, CreateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'themes/theme_form.html'
    success_url = reverse_lazy('tasks:workshop')

    def form_valid(self, form):
        form.instance.user = self.request.user   # 🔑 Прив’язуємо автора
        return super().form_valid(form)


class ThemeUpdateView(LoginRequiredMixin, UpdateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'themes/theme_form.html'
    success_url = reverse_lazy('tasks:workshop')

    def form_valid(self, form):
        # гарантуємо, що користувач не зміниться
        form.instance.user = self.request.user
        return super().form_valid(form)


class ThemeDeleteView(LoginRequiredMixin, DeleteView):
    model = Theme
    template_name = 'themes/theme_confirm_delete.html'
    success_url = reverse_lazy('tasks:workshop')

    def get_queryset(self):
        # щоб можна було видаляти лише свої теми
        return Theme.objects.filter(user=self.request.user)
class ThemeAddView(LoginRequiredMixin, View):
    """
    Додає тему користувачу або активує її, якщо вже додана.
    """
    def get(self, request, pk):
        # Знаходимо оригінальну тему
        original_theme = get_object_or_404(Theme, pk=pk)

        # Перевіряємо, чи така тема вже є у користувача (по оригінальному ID)
        user_theme = Theme.objects.filter(
            user=request.user,
            workshop=original_theme.workshop
        ).first()

        # Якщо тема вже є → активуємо її
        if user_theme:
            Theme.objects.filter(user=request.user).update(is_active=False)
            user_theme.is_active = True
            user_theme.save()
        else:
            # Якщо теми немає → створюємо копію та активуємо її
            Theme.objects.filter(user=request.user).update(is_active=False)
            Theme.objects.create(
                user=request.user,
                name=original_theme.name,
                description=original_theme.description,
                workshop=original_theme.workshop,
                primary_color=original_theme.primary_color,
                secondary_color=original_theme.secondary_color,
                font_family=original_theme.font_family,
                background_image=original_theme.background_image,
                is_active=True
            )

        return redirect('tasks:workshop')


# --- NOTES ---
class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'tasks/note_create.html'
    success_url = reverse_lazy('tasks:note-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'tasks/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(creator=self.request.user)
