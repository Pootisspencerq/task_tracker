from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView  # <-- додано

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Основні аплікації
    path('', include('tasks.urls')),             # Теми та воркшоп
    path('auth/', include('auth_system.urls')),  # Логін, реєстрація
    
    # Login/Logout
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Перенаправлення /login/ на правильний шлях
    path('signin/', RedirectView.as_view(url='/login/')),  # якщо хочеш альтернативний шлях
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
