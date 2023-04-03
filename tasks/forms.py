from django.forms import ModelForm

from .models import Task, Comment

class TaskForm(ModelForm):
    class Meta:
        model = Task 
        fields = ['title', 'description','priority','dedline_task']


class StageUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['stage',]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

