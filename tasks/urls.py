from django.urls import path
from .views import (
    TaskListView,
    ThemeEditorView,
    ThemeWorkshopView,
    ThemeUpdateView,
    ThemeDeleteView,
    ThemeAddView,
    NoteCreateView,
    NoteListView
)
from django.conf import settings
from django.conf.urls.static import static
from .views import NoteCreateView, NoteListView
from .import views 
app_name = 'tasks'
urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path("task/create/", views.TaskCreateView.as_view(), name='task-create'),
    path("task/<int:pk>/update",views.TaskUpdateView.as_view(), name='task-update'),
    path("task/<int:pk>/delete",views.TaskDeleteView.as_view(), name='task-delete'),
    # Замітки
    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/create/', NoteCreateView.as_view(), name='note-create'),

    # Теми
    path('themes/editor/', ThemeEditorView.as_view(), name='editor'),
    path('themes/workshop/', ThemeWorkshopView.as_view(), name='workshop'),
    path('themes/<int:pk>/update/', ThemeUpdateView.as_view(), name='theme-update'),
    path('themes/<int:pk>/delete/', ThemeDeleteView.as_view(), name='theme-delete'),
    path('themes/<int:pk>/add/', ThemeAddView.as_view(), name='add-user-theme'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
