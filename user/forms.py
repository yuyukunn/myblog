from django import forms
from django.contrib.auth.models import User

class RegForm(forms.Form):
	username = forms.CharField(
		label = '用户名',
		max_length=20,
		min_length=3,
		widget=forms.TextInput(
			attrs={'class':'form-control','placeholder':'请输入用户名'}
		)
	)
	email = forms.EmailField(
		label = '邮箱',
		widget=forms.EmailInput(
			attrs={'class':'form-control','placeholder':'请输入正确的邮箱'}
		)
	)
	verification_code = forms.CharField(
		label = '验证码',
		widget=forms.TextInput(
			attrs={'class':'form-control','placeholder':'点击“发送验证码”发送到邮箱'}
		)
	)
	password = forms.CharField(
		label = '密码',
		min_length=6,
		widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请输入密码'}
		)
	)
	password_again = forms.CharField(
		label = '再输入一次密码',
		min_length=6,
		widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请再一次输入密码'}
		)
	)
	def __init__(self,data,request):
		self.request = request
		super().__init__(data,request)


	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('用户名已存在')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('该邮箱已存在')
		return email

	def clean(self):
		if self.request:
			code = self.request.session.get('register')
			verification_code = self.cleaned_data.get('verification_code')
			if (code and code != verification_code) or not code:
				raise forms.ValidationError('验证码不正确')

	def clean_password_again(self):
		password = self.cleaned_data['password']
		password_again = self.cleaned_data['password_again']
		if password != password_again:
			raise forms.ValidationError('两次输入的密码不一致')
		return password_again

	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code','').strip()
		if not verification_code:
			raise forms.ValidationError('验证码不能为空')
		return verification_code

class LoginForm(forms.Form):
	username = forms.CharField(
		label="用户名",
		max_length=16,
		required=True,
		widget=forms.TextInput(attrs={'class':'form-control'}),
	)
	password = forms.CharField(
		label="密码",
		min_length=6,
		required=True,
		widget=forms.PasswordInput(attrs={'class':'form-control'}),
	)
	
class ChangeNicknameForm(forms.Form):
	new_nickname = forms.CharField(
			label = '新的昵称',
			max_length=20,
			widget=forms.TextInput(
				attrs={'class':'form-control','placeholder':'请输入新的昵称'}
				)
		)

	def clean_nickname_new(self):
		new_nickname = self.cleaned_data.get('new_nickname','').strip()
		if new_nickname == '':
			raise ValidationError('新的昵称不能为空')
		return new_nickname

class BindEmailForm(forms.Form):
	email = forms.EmailField(
			label = '邮箱',
			widget=forms.EmailInput(
				attrs={'class':'form-control','placeholder':'请输入正确的邮箱'}
				)
		)
	verification_code = forms.CharField(
			label = '验证码',
			widget=forms.TextInput(
				attrs={'class':'form-control','placeholder':'点击“发送验证码”发送到邮箱'}
				)
		)

	def __init__(self,data,request):
		self.request = request
		super().__init__(data,request)
	def clean(self):
		if self.request:
			if self.request.user.email:
				raise forms.ValidationError('你已绑定邮箱')

			code = self.request.session.get('bind_email')
			verification_code = self.cleaned_data.get('verification_code')
			if (code and code != verification_code) or not code:
				raise forms.ValidationError('验证码不正确')

	# 验证邮箱是否存在
	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('该邮箱已存在')
		return email

	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code').strip()
		if not verification_code:
			raise forms.ValidationError('验证码不能为空')
		return verification_code

class ChangePwdForm(forms.Form):
	old_password = forms.CharField(
		label = '旧的密码',
		min_length=6,
		widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请输入旧的密码'}
		)
	)
	new_password = forms.CharField(
		label = '新的密码',
		min_length=6,
		widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请输入新的密码'}
		)
	)
	new_password_again = forms.CharField(
		label = '请再次输入新的密码',
		min_length=6,
		widget=forms.PasswordInput(
			attrs={'class':'form-control','placeholder':'请再次输入新的密码'}
		)
	)

	def __init__(self,data,user):
		self.user = user
		super().__init__(data,user)

	def clean(self):
		# 验证两次密码是否一致
		new_password = self.cleaned_data.get('new_password')
		new_password_again = self.cleaned_data.get('new_password_again')
		if new_password != new_password_again or new_password == '':
			raise forms.ValidationError('两次输入的密码不一致')
		return self.cleaned_data

	def clean_old_password(self):
		# 验证旧密码是否正确
		if self.user:
			old_password = self.cleaned_data.get('old_password')
			if not self.user.check_password(old_password):
				raise forms.ValidationError('旧的密码错误')
			return old_password