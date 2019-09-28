from django.contrib import admin
from django.urls import path,re_path,include
from user import views

urlpatterns = [
	path('register/',views.reg),
	path('login/',views.login),
	path('logout/',views.logout),
    path('change_nickname/',views.change_nickname),
    path('change_password/',views.change_password),    
    path('user_info/',views.user_info),
    path('bind_email/',views.bind_email),
    path('send_verification_code/',views.send_verification_code),
]
