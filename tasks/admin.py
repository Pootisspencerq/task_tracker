from django.contrib import admin
from tasks.models import Task, Comment, Note, Theme

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Note)
admin.site.register(Theme)