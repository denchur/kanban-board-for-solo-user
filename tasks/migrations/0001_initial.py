# Generated by Django 2.2.19 on 2023-02-28 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название задчи')),
                ('description', models.TextField(verbose_name='Описание задчи')),
                ('start_task', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания задчи')),
                ('complate_task', models.DateTimeField(null=True, verbose_name='Дата завершения задчи')),
                ('priority', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.Priority', verbose_name='Приоритет задачи')),
                ('stage', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='tasks.Stage', verbose_name='Стадия выполнения задачи')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Владелец задачи')),
            ],
            options={
                'ordering': ['-priority'],
            },
        ),
    ]
