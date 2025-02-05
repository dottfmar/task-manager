from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Task, Team, Worker, Position, TaskType, Project


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = ('username', 'email', "first_name", "last_name", "position")
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'position'),
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    ...

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    ...

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    ...

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ...

@admin.register(Position)
class Position(admin.ModelAdmin):
    ...