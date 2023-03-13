from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='home_page'),
    path('tasks/<str:username>/', views.tasks, name='tasks'),
    path('task/<int:task_id>/', views.task, name='task_detail'),
    path('create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:task_id>/update-stage/', views.stage_update, name='update_stage'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]