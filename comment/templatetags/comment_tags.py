from django import template
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm
from user.models import Profile
register = template.Library()

@register.simple_tag
def get_comment_count(obj):
	content_type = ContentType.objects.get_for_model(obj)
	return Comment.objects.filter(content_type=content_type,object_id=obj.pk).count()

@register.simple_tag
def get_comment_form(obj):
	content_type = ContentType.objects.get_for_model(obj)
	form = CommentForm(initial={
			'content_type':content_type.model,
			'object_id':obj.pk,
			'reply_comment_id':0
		})
	return form

@register.simple_tag
def get_comment_list(obj):
	content_type = ContentType.objects.get_for_model(obj)
	comments = Comment.objects.filter(object_id=obj.pk,parent=None).order_by('comment_time')
	return comments

@register.simple_tag
def get_reply_list(obj):
	content_type = ContentType.objects.get_for_model(obj)
	comments = Comment.objects.filter(object_id=obj.pk,parent__gt=0).order_by('comment_time')
	return comments

@register.simple_tag
def get_nickname(user):
	obj = Profile.objects.filter(user=user).first()
	if obj:
		return obj.user.username+'('+obj.nickname+')' if obj.nickname else obj.user


