from django.contrib import admin
from blog import models
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
	"""docstring for BlogAdmin"""
	list_display = ('id','title','read_num','author','create_time','last_updated_time')

class BlogTypeAdmin(admin.ModelAdmin):
	"""docstring for BlogTypeAdmin"""
	list_display = ('type_name',)
		
class ReadNumAdmin(admin.ModelAdmin):
	"""docstring for BlogTypeAdmin"""
	list_display = ('readnum','blog')

class ReadNumDateAdmin(admin.ModelAdmin):
	"""docstring for BlogTypeAdmin"""
	list_display = ('readnum_date','date_time','blog')		

admin.site.register(models.Blog,BlogAdmin)
admin.site.register(models.BlogType,BlogTypeAdmin)
admin.site.register(models.ReadNum,ReadNumAdmin)
admin.site.register(models.ReadNumDate,ReadNumDateAdmin)
