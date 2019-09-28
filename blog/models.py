from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
# Create your models here.


class Blog(models.Model):
	title = models.CharField(max_length=32)
	content = RichTextUploadingField()
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	create_time = models.DateTimeField(auto_now_add=True)
	last_updated_time = models.DateTimeField(auto_now=True)
	blog_type = models.ForeignKey('BlogType',on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def read_num(self):
		try:
			return self.readnum.readnum
		except Exception as e:
			return 0
	
	class Meta:
		ordering = ['-create_time']

class BlogType(models.Model):
	type_name = models.CharField(max_length=16)
	def __str__(self):
		return self.type_name


class ReadNum(models.Model):
	"""docstring for ReadNum"""
	readnum = models.IntegerField(default=0)
	blog = models.OneToOneField('Blog',on_delete=models.CASCADE)


class ReadNumDate(models.Model):
	readnum_date = models.IntegerField(default=0)
	date_time = models.DateTimeField(default=timezone.now)
	blog = models.OneToOneField('Blog',on_delete=models.CASCADE)
	class Meta:
		ordering = ['-date_time']

		