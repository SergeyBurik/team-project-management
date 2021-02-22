from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from mainapp.models import Board, Teammate, Column, Task

admin.site.register(Board)
admin.site.register(Teammate)
admin.site.register(Task)
admin.site.register(Column)