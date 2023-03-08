from django.forms import ModelForm

from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task 
        fields = ['title', 'description','stage','priority','start_task']


class StageUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['stage','complate_task']

