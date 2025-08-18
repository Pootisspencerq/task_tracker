from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progres', 'In Progress'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    comment_to_task = models.TextField()

    def __str__(self):
        return f"Comment on {self.task.title}"

class Theme(models.Model):
    name = models.CharField(max_length=100)
    background_color = models.CharField(max_length=7, default="#ffffff")
    text_color = models.CharField(max_length=7, default="#000000")
    custom_css = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='themes/images/', blank=True, null=True)
    font_family = models.CharField(max_length=100, default="sans-serif")

class Note(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='notes/images/', blank=True, null=True)  # <-- картинка
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()  # раніше було comment_to_task
    image = models.ImageField(upload_to='comments/images/', blank=True, null=True)  # якщо потрібна картинка

    def __str__(self):
        return f"Comment on {self.task.title}"
