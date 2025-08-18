from django import forms
from tasks.models import Task, Comment, Theme, Note


# ---------- Task Forms ----------
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['due_date'].widget.attrs['class'] += ' my-custom-datepicker'


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'Всі'),
        ('todo', 'To Do'),
        ('in_progres', 'In Progress'),
        ('done', 'Done')
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='Статус')

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})


# ---------- Theme Form ----------
class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = [
            'name',
            'background_color',
            'text_color',
            'background_image',
            'font_family',
            'custom_css',
        ]
        widgets = {
            'background_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'text_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'font_family': forms.TextInput(attrs={'class': 'form-control'}),
            'custom_css': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(ThemeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['background_color', 'text_color', 'custom_css', 'font_family']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})


# ---------- Note Form ----------
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['task', 'title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


# ---------- Comment Form ----------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['task', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
