from django.urls import path,re_path
from comment import views

urlpatterns = [
	path('',views.update_comment,name="update_comment"),
]