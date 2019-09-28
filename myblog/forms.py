from django import forms
from django.contrib.auth.models import User
class LoginForm(forms.Form):
	username = forms.CharField(
								label="用户名",
								max_length=16,
								required=True,
								# error_message={
								# 	'required':'用户名不能为空'
								# },
								widget=forms.TextInput(
									attrs={
										'class':'form-control',
									}
								),
	)
	password = forms.CharField(
								label="密码",
								min_length=8,
								required=True,
								widget=forms.PasswordInput(
									attrs={
										'class':'form-control',
									}
								),
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
			raise forms.ValidationError('新的昵称不能为空')
		return new_nickname


