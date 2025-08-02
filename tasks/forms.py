from django import forms
from tasks.models import Task, Comment, Note
from tasks.models import Theme
from .models import Theme, Workshop

class ThemeForm(forms.ModelForm):
    workshop = forms.ModelChoiceField(
        queryset=Workshop.objects.none(),  # default empty, will set in __init__
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label='Майстерня'
    )

    class Meta:
        model = Theme
        fields = [
            'name', 'description', 'workshop',
            'primary_color', 'secondary_color', 'font_family', 'background_image'
        ]
        # widgets as above

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['workshop'].queryset = Workshop.objects.filter(
                owner=user
            ) | Workshop.objects.filter(members=user)
        else:
            self.fields['workshop'].queryset = Workshop.objects.all()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'image', 'workshop', 'shared_with']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'shared_with': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'Всі'),
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='Статус')

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content', 'image']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
