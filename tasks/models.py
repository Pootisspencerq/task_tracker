from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=255, verbose_name="Назва Завданнь")
    description = models.TextField(blank=True, verbose_name="Опис Завданнь")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo', verbose_name="Статус Завданнь")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Пріоритет Завданнь")
    due_date = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Theme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="themes")
    name = models.CharField(max_length=100)
    background_color = models.CharField(max_length=7, default="#ffffff")
    text_color = models.CharField(max_length=7, default="#000000")
    custom_css = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='themes/images/', blank=True, null=True)
    font_family = models.CharField(max_length=100, default="sans-serif")
    is_active = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    workshop = models.TextField(blank=True, null=True)
    primary_color = models.CharField(max_length=7, default="#0000ff")
    secondary_color = models.CharField(max_length=7, default="#00ff00")

    def save(self, *args, **kwargs):
        if self.user:  # тільки якщо є користувач
            # Якщо це перша тема користувача — робимо активною
            if not Theme.objects.filter(user=self.user).exists():
                self.is_active = True

            if self.is_active:
                # скинути інші теми користувача
                Theme.objects.filter(user=self.user, is_active=True).exclude(pk=self.pk).update(is_active=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = self.user
        was_active = self.is_active
        super().delete(*args, **kwargs)

        # Якщо видалили активну тему → призначити будь-яку іншу
        if was_active and user:
            next_theme = Theme.objects.filter(user=user).first()
            if next_theme:
                next_theme.is_active = True
                next_theme.save()

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Note(models.Model):
   
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='notes/images/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    image = models.ImageField(upload_to='comments/images/', blank=True, null=True)

    def __str__(self):
        return f"Comment on {self.task.title}"
