from django.contrib import admin
from .models import Task
# Register your models here.

class AdminTask(admin.ModelAdmin):
	data_hierarchy="date"
	search_fields=['title','created_by']
	list_display=('title','completed','favorite','date',)
	list_filter=('favorite','completed')

admin.site.register(Task,AdminTask)
