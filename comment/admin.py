from django.contrib import admin
from comment import models
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
	"""docstring for BlogTypeAdmin"""
	list_display = ('text','comment_time','user','id','reply_to','root','parent')		

admin.site.register(models.Comment,CommentAdmin)
