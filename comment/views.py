from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import time
from comment import forms
from comment import models
# Create your views here.

def update_comment(request):
	data = {'status':True,'msg':None}
	comment_form = forms.CommentForm(request.POST,user=request.user)
	if comment_form.is_valid():
		comment_obj = models.Comment()
		comment_obj.object_id = comment_form.cleaned_data['object_id']
		comment_obj.user = comment_form.cleaned_data['user']
		comment_obj.text = comment_form.cleaned_data['comment_text']
		comment_obj.content_object = comment_form.cleaned_data['comment_obj']
		comment_obj.img_id = comment_form.cleaned_data['img_id']
		parent = comment_form.cleaned_data['parent']
		if parent:
			comment_obj.root = parent.root if parent.root else parent
			comment_obj.parent = parent
			comment_obj.reply_to = parent.user
		comment_obj.save()
		data['img_id'] = comment_obj.img_id
		data['username'] = comment_obj.user.username
		data['text'] = comment_obj.text
		data['comment_time'] = time.strftime(r"%Y-%m=%d` %H:%M",time.localtime())
		data['comment_time'] = data['comment_time'].replace('-','年').replace('=','月').replace('`','日')
		if parent:
			data['reply_to'] = comment_obj.reply_to.username
		else:
			data['reply_to'] = ''
		data['pk'] = comment_obj.pk

	else:
		data['status']=False
		data['msg'] = '评论不能为空'
	return JsonResponse(data)