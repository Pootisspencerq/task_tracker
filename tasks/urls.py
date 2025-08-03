from django.urls import path
from .views import (
    TaskListView, TaskDetailView, TaskUpdateView, TaskDeleteView,
    TaskCreateView, TaskCompleteView,
    ThemeEditorView, ThemeWorkshopView
)

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/complete/', TaskCompleteView.as_view(), name='task-complete'),
    path('themes/editor/', ThemeEditorView.as_view(), name='editor'),
    path('themes/workshop/', ThemeWorkshopView.as_view(), name='workshop'),
]
