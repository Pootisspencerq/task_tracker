from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.TaskListView.as_view(), name ='task-list'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name ='task-detail'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name ='task-update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name ='task-delete'),
    path('task-create/', views.TaskCreateView.as_view(), name ='task-create'),
    path('<int:pk>/complete/', views.TaskCompleteView.as_view(), name='task-complete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = 'tasks'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)