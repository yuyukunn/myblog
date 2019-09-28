from django.shortcuts import render,get_object_or_404,HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import json
import datetime
from django.db.models import Max,Sum,Count
from blog import models as b_models
from comment import forms,models
# Create your views here.
class PageInfo(object):
	def __init__(self,current_page,per_page,blog_total):
		try:
			self.current_page = int(current_page)
		except:
			self.current_page = 1
		self.per_page = per_page
		self.blog_total = blog_total
		self.pages = 0

	def page_show(self):
		page_style = []
		self.pages,n = divmod(self.blog_total,self.per_page)
		if n:
			self.pages += 1
		for i in range(1,self.pages+1):
			if i == self.current_page:
				p = r'<li class="active"><a href="/blog/page/%s">%s</a></li>' % (i,i)
			else:
				p = r'<li><a href="/blog/page/%s">%s</a></li>' % (i,i)
			page_style.append(p)
		return page_style

	def start(self):
		return (self.current_page-1)*self.per_page

	def end(self):
		return self.current_page*self.per_page

	def page_show_better(self):
		page_style = self.page_show()
		begin = max(self.current_page-3,0)
		stop = min(self.current_page+2,self.pages)
		page_style = page_style[begin:stop]
		first = r'<li><a href="/blog/page/1">首页</a></li>'
		pre = r'<li><a href="/blog/page/%s">上一页</a></li>' % max(self.current_page-1,1)
		page_style.insert(0,first)
		page_style.insert(1,pre)
		last = r'<li><a href="/blog/page/%s">尾页</a></li>' % self.pages
		ne = r'<li><a href="/blog/page/%s">下一页</a></li>' % min(self.current_page+1,self.pages)
		page_style.append(ne)
		page_style.append(last)
		return ''.join(page_style)


def blog_list(request,current_page=1):
	blog_dict = get_data()
	p = PageInfo(current_page,5,blog_dict['blogs'].count())
	show_page = p.page_show_better()
	blog_dict['classify'] = '博客主页'
	blog_dict['blogs'] = blog_dict['blogs'][p.start():p.end()]
	blog_dict['show_page'] = show_page
	blog_dict['current_page'] = p.current_page
	return render(request,'blog_list.html',blog_dict)

def blog_with_type(request,type_id,current_page=1):
	blog_dict = get_data()
	p = PageInfo(current_page,5,blog_dict['blogs'].filter(blog_type_id=type_id).count())
	show_page = p.page_show_better().replace('/blog/page/','/blog/type%s/page/' % type_id)
	blog_type = get_object_or_404(b_models.BlogType,pk=type_id)
	blog_dict['classify'] = '分类'
	blog_dict['blogs'] = blog_dict['blogs'].filter(blog_type_id=type_id)[p.start():p.end()]
	blog_dict['blog_type'] = blog_type
	blog_dict['show_page'] = show_page
	blog_dict['current_page'] = p.current_page
	return render(request,'blog_with_type.html',blog_dict)

def blog_with_date(request,year,month,current_page=1):
	blog_dict = get_data()	
	p = PageInfo(current_page,5,blog_dict['blogs'].filter(create_time__year=year,create_time__month=month).count())
	show_page = p.page_show_better().replace('/blog/page/','/blog/date/%s-%s/page/' % (year,month))
	blog_dict['classify'] = '时间'
	blog_dict['blogs'] = blog_dict['blogs'].filter(create_time__year=year,create_time__month=month)[p.start():p.end()]
	blog_dict['date'] = '%s年%s月' % (year,month)
	blog_dict['show_page'] = show_page
	blog_dict['current_page'] = p.current_page
	return render(request,'blog_with_date.html',blog_dict)

def blog_details(request,nid):
	blog_dict = {}
	blog_obj = readnum_add(request,nid)
	blog_dict['blog_obj'] = blog_obj
	blog_dict['pre_blog'] = b_models.Blog.objects.filter(create_time__gt=blog_obj.create_time).last()
	blog_dict['next_blog'] =b_models.Blog.objects.filter(create_time__lt=blog_obj.create_time).first()
	blog_dict['user'] = request.user
	response = render(request,'blog_details.html',blog_dict)
	response.set_cookie('blog_%s_read' % nid,'true',max_age=60)
	return response

def readnum_add(request,nid):
	blog_obj = get_object_or_404(b_models.Blog,pk=nid)
	if not request.COOKIES.get('blog_%s_read' % nid):  # 计数加一
		if b_models.ReadNum.objects.filter(blog=blog_obj).count():
			readnum = b_models.ReadNum.objects.get(blog=blog_obj)
		else:
			readnum = b_models.ReadNum()
			readnum.blog = blog_obj
		readnum.readnum += 1
		readnum.save()
		# 每天的阅读次数
		readnumdates = b_models.ReadNumDate.objects.all()
		for readnumdate in readnumdates:
			if readnumdate.date_time.date() == timezone.now().date() and readnumdate.blog==blog_obj:
				readnumdate.readnum_date += 1
				readnumdate.save()
				break
		else:
			b_models.ReadNumDate.objects.create(date_time=timezone.now(),readnum_date=1,blog=blog_obj)
	return blog_obj

def get_data():
	blog_dict = {}
	blog_dates_dict ={}
	blogs = b_models.Blog.objects.all()
	blog_types = b_models.BlogType.objects.all()
	dates = blogs.dates('create_time','month','DESC').distinct()

	for date in dates:
		count = blogs.filter(create_time__year=date.year,create_time__month=date.month).count()
		blog_dates_dict[date] = count
	
	blog_dict['blog_dates'] = blog_dates_dict
	blog_dict['blog_types'] = blog_types
	blog_dict['blogs'] = blogs
	return blog_dict