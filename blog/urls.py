from django.urls import path,re_path
from blog import views


urlpatterns = [
	path('',views.blog_list,name="home"),
	re_path(r'page/(\d+)/',views.blog_list,name="page"),

    re_path(r'(\d+).html/', views.blog_details, name="blog_details"),
    re_path(r'type(\d+)/page/(\d+)?', views.blog_with_type, name="blog_with_type"),
    re_path(r'date/(\d+)-(\d+)/page/(\d+)?',views.blog_with_date, name="blog_with_date"),
]