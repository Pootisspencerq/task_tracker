from django import forms
from tasks.models import Task, Comment, Theme

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_to_task']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['due_date'].widget.attrs['class'] += ' my-custom=datepicker'


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


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'background_color', 'text_color', 'background_image']
        widgets = {
            'background_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'text_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        }

    def __init__(self, *args, **kwargs):
        super(ThemeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['background_color', 'text_color']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
