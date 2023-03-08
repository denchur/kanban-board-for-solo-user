from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, User, Stage
from .forms import TaskForm, StageUpdateForm


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('tasks:tasks', request.user)
    else: 
        return redirect('users:login')


def tasks(request, username):
    if request.user.is_authenticated == False:
        return redirect('users:login')
    worker = get_object_or_404(User, username = username)
    worker_task = Task.objects.filter(worker = worker)
    if request.user == worker:
        task_stage_one = worker_task.filter(stage = 1)
        task_stage_two = worker_task.filter(stage = 2)
        task_stage_three = worker_task.filter(stage = 3)
        task_stage_four = worker_task.filter(stage = 4)
        context = {
            'task_stage_one': task_stage_one,
            'task_stage_two': task_stage_two,
            'task_stage_three': task_stage_three,
            'task_stage_four': task_stage_four,
            'worker': worker,
            'worker_task': worker_task,
        }
        return render(request, 'tasks/tasks.html', context)
    else:
        return redirect('tasks:tasks', request.user)


def task(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    stage = Stage.objects.all()
    context = {
        'task': task,
        'stage': stage,
    }
    return render(request, 'tasks/task_detail.html', context)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit = False)
            task.worker = request.user
            task.save()
            return redirect('tasks:tasks', request.user)
    else:
        form = TaskForm()
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'tasks/task_create.html', context)


def task_edit(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    worker = task.worker
    if request.user == worker:
        form = TaskForm(request.POST or None, instance = task)
        if request.method == 'POST' and form.is_valid:
            task = form.save()
            return redirect('tasks:tasks', request.user)
        context = {
            'form': form,
            'is_edit': True,
            'task': task,
        }
        return render(request, 'tasks/task_create.html', context)
    if request.user != worker:
        return redirect('tasks:tasks', request.user)


def stage_update(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    worker = task.worker
    if request.user == worker:
        form = StageUpdateForm(request.POST or None, instance = task)
        if request.method == 'POST' and form.is_valid:
            task = form.save()
            return redirect('tasks:tasks', request.user)
        context = {
            'form': form,
            'is_update_stage': True,
            'task': task,
        }
        return render(request, 'tasks/task_create.html', context)
    if request.user != worker:
        return redirect('tasks:tasks', request.user)
    

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    worker = task.worker
    if request.user == worker:
        task.delete()
        return redirect('tasks:tasks', request.user)
    if request.user != worker:
        return redirect('tasks:tasks', request.user)










