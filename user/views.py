import string
import datetime
import random
import time
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from user import models,forms
from blog import models as b_models
from django.core.mail import send_mail
# Create your views here.

def reg(request):
	context = {}
	context['return_to'] = request.META.get('HTTP_REFERER')
	context['extra_content'] = '<button type="button" style="margin-top:1em;margin-left:2em;" id="send_code" class="btn btn-primary">发送验证码</button>'
	if request.method == 'GET':
		reg_form = forms.RegForm(data=None,request=None)
		context['reg_form'] = reg_form
		return render(request,'register.html',context)
	else:
		reg_form = forms.RegForm(data=request.POST,request=request)
		if reg_form.is_valid():
			username = reg_form.cleaned_data['username']
			email = reg_form.cleaned_data['email']
			password = reg_form.cleaned_data['password']
			# 创建用户
			user = auth.models.User.objects.create_user(username,email,password)
			user.save()
			# 清除session
			del request.session['register']
			# 登录
			user = auth.authenticate(username=username,password=password)
			auth.login(request,user)
			if request.POST.get('return_to') == 'None':
				return redirect('/')
			else:
				return redirect(request.POST.get('return_to'))
		else:
			context['reg_form'] = reg_form
			return render(request,'register.html',context)

def login(request):
	if request.method == 'GET':
		context = {}
		login_form = forms.LoginForm()
		context['login_form'] = login_form
		context['return_to'] = request.META.get('HTTP_REFERER')
		context['user'] = request.user
		return render(request,'login.html',context)
	else:
		login_form = forms.LoginForm(request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data.get('username')
			password = login_form.cleaned_data.get('password')
			user = auth.authenticate(request,username=username,password=password)
			if user:
				auth.login(request,user)
				if request.POST.get('return_to') == 'None':
					return redirect('/')
				else:
					return redirect(request.POST.get('return_to'))
					
			else:
				login_form.add_error(None,'用户名或密码不正确')
				return render(request,'login.html',{'login_form':login_form})

def logout(request):
	auth.logout(request)
	return redirect('/')

def change_nickname(request):
	if request.method == 'POST':
		form = forms.ChangeNicknameForm(request.POST)
		if form.is_valid():
			new_nickname = form.cleaned_data['new_nickname']
			profile,created = models.Profile.objects.get_or_create(user=request.user)
			profile.nickname = new_nickname
			profile.save()
			return redirect('/user/user_info/')
	else:
		form = forms.ChangeNicknameForm()
	context = {}
	context['form'] = form
	context['page_title'] = '修改昵称'
	context['submit_text'] = '修改'
	context['form_title'] = '修改昵称'
	context['return_to'] = "/user/user_info/"
	context['user'] = request.user
	return render(request,'form.html',context)

def user_info(request):
	series = {}
	home_info ={}
	series['name'] = '阅读量'
	today = datetime.date.today()
	q = b_models.ReadNumDate.objects.filter(date_time__range=(today - datetime.timedelta(days=7), \
										  today+datetime.timedelta(days=1))).values('date_time','readnum_date')
	stack_date = []
	for i in range(7):
		date = today - datetime.timedelta(days=i)
		s = str(date.month)+'/'+str(date.day)
		stack_date.append(s)
	stack_count = [0,0,0,0,0,0,0]
	for d in q:
		if d.get('date_time'):
			s = str(d.get('date_time').month)+'/'+str(d.get('date_time').day)
			i = 0
			while i < len(stack_date):
				if s==stack_date[i]:
					stack_count[i] += int(d.get('readnum_date'))
				i += 1
	home_info = {}
	series['data'] = stack_count[::-1]
	home_info['series'] = [series]
	home_info['date_list'] = stack_date[::-1]
	return render(request,'user_info.html',home_info)

def bind_email(request):
	if request.method == 'POST':
		form = forms.BindEmailForm(request.POST,request)
		if form.is_valid():
			# clean(form.cleaned_data,request)
			email = form.cleaned_data['email']
			request.user.email = email
			request.user.save()
			del request.session['bind_email']
			return redirect('/user/user_info/')
	else:
		form = forms.BindEmailForm(data=None,request=None)
	context = {}
	context['form'] = form
	context['page_title'] = '绑定邮箱'
	context['submit_text'] = '绑定'
	context['form_title'] = '绑定邮箱'
	context['return_to'] = "/user/user_info/"
	context['user'] = request.user
	context['extra_content'] = '<button type="button" style="margin-top:1em;margin-right:1em;" id="send_code" class="btn btn-primary pull-right">发送验证码</button>'
	return render(request,'form.html',context)

def send_verification_code(request):
	data = {}
	code_send_for = request.GET.get('code_send_for','')
	email = request.GET.get('email','')
	if email:
		# 生成验证码
		code = ''.join(random.sample(string.ascii_letters+string.digits,4))
		now = int(time.time())
		send_code_time = request.session.get('send_code_time',0)
		if now - send_code_time < 30:
			data['status'] = False
			data['msg'] = '请求过于频繁，请稍后再试'
		else:
			request.session[code_send_for] = code
			request.session['send_code_time'] = now
		send_mail(
			'绑定邮箱',
			'验证码：%s' % code,
			'983249451@qq.com',
			[email],
			fail_silently=False,
		)
		data['status'] = True
	else:
		data['status'] = False
		data['msg'] = '邮箱不能不空'
	return JsonResponse(data)

def change_password(request):
	if request.method == 'POST':
		form = forms.ChangePwdForm(data=request.POST,user=request.user)
		if form.is_valid():
			user = request.user
			old_password = form.cleaned_data['old_password']
			new_password = form.cleaned_data['new_password']
			user.set_password(new_password)
			user.save()
			logout(request)
			return redirect('/user/login/')
	else:
		form = forms.ChangePwdForm(data=None,user=None)
	context = {}
	context['form'] = form
	context['page_title'] = '修改密码'
	context['submit_text'] = '修改'
	context['form_title'] = '修改密码'
	context['return_to'] = "/user/user_info/"
	context['user'] = request.user
	return render(request,'form.html',context)
