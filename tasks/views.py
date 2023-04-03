import datetime 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Task, Stage
from .forms import TaskForm, StageUpdateForm, CommentForm

User = get_user_model()
def index(request):
    if request.user.is_authenticated:
        return redirect('tasks:tasks', request.user)
    else: 
        return redirect('users:login')


@login_required
def tasks(request, username):
    worker = get_object_or_404(User, username = username)
    worker_task = Task.objects.filter(worker = worker)
    now = datetime.datetime.now()
    date = now.date()
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
            'date':date,
        }
        return render(request, 'tasks/tasks.html', context)
    else:
        return redirect('tasks:tasks', request.user)

@login_required
def add_comment(request, task_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.task = get_object_or_404(Task, pk=task_id)
        comment.save()
    return redirect('tasks:task_detail', task_id=task_id)


def task(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    form = CommentForm()
    comments =  task.comments.all()
    if request.user == task.worker:
        stage = Stage.objects.all()
        context = {
            'task': task,
            'stage': stage,
            'comments':comments,
            'form': form,
        }
        return render(request, 'tasks/task_detail.html', context)
    else:
        return redirect('tasks:tasks', request.user)

@login_required
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

@login_required
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

@login_required
def stage_update(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    now = datetime.datetime.now()
    
    worker = task.worker
    if request.user == worker:
        form = StageUpdateForm(request.POST or None, instance = task)
        if request.method == 'POST' and form.is_valid:
            tasks = form.save(commit = False)
            tasks.complate_task= now.date()
            task.save()
            return redirect('tasks:tasks', request.user)
        context = {
            'form': form,
            'is_update_stage': True,
            'task': task,
        }
        return render(request, 'tasks/task_create.html', context)
    if request.user != worker:
        return redirect('tasks:tasks', request.user)
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    worker = task.worker
    if request.user == worker:
        task.delete()
        return redirect('tasks:tasks', request.user)
    if request.user != worker:
        return redirect('tasks:tasks', request.user)










