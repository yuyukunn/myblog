from django.shortcuts import render,redirect,HttpResponse
from django.utils import timezone
import datetime
from django.contrib.auth.models import AnonymousUser
from django.db.models import Max,Sum
from blog import models
from user import models as u_models
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from .forms import *
# Create your views here.
def homepage(request):
	home_info = {}	
	# 缓存
	# sevenday_hot_cache = cache.get('sevenday_hot')
	# if not sevenday_hot_cache:
	# 	sevenday_hot_cache = get_hot_sevenday()
	# 	cache.set('sevenday_hot',sevenday_hot_cache,60*60)
	# 行业统计数据
	# xAxis,amount,market_cap,market_equity,date = industry_trend()
	# home_info['subtitle'] = '时间：（%s）' % date
	# home_info['xAxis'] = xAxis
	# home_info['amount'] = amount
	# home_info['market_cap'] = market_cap
	home_info['today_hot'] = get_hot_today()
	home_info['aph'] = get_aphorism()
	home_info['yesterday_hot'] = get_hot_yesterday()
	home_info['sevenday_hot'] = get_hot_sevenday()
	return render(request,'welcome.html',home_info)

def get_hot_today():
	"""获取当天热门博客数据"""
	today = timezone.now().date()
	q = models.ReadNumDate.objects.filter(date_time__date=today).order_by('-readnum_date').first()
	return q

def get_hot_yesterday():
	yesterday = timezone.now().date()-datetime.timedelta(days=1)
	q = models.ReadNumDate.objects.filter(date_time__date=yesterday).order_by('-readnum_date').first()
	return q

def get_hot_sevenday():
	today = datetime.date.today()
	q = models.ReadNumDate.objects.filter(date_time__range=(today - datetime.timedelta(days=7), \
									      today+datetime.timedelta(days=1)))\
								  .values('blog','blog__title')\
								  .annotate(read_num_sum=Sum('readnum_date'))\
								  .order_by('-read_num_sum')
	return q[:5]

def industry_trend():
	import requests
	import re
	# 深圳证券交易所网址
	url = 'http://www.szse.cn/market/stock/deal/index.html'
	headers = {
	    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit"
	                  "/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
	}
	response = requests.get(url=url, headers=headers)
	html = response.content.decode('utf-8')
	# 由于网站的数据是通过api接口获取，因此需找到api接口，通过观察，数据是通过catalog_id获取的
	# 同时又发现，data-s-catalog-id与其一直，因此需要获取data-s-catalog-id的值
	catalog_id = re.findall(r'data-s-catalog-id="(.+?)"', html, re.DOTALL)[0]

	if catalog_id:
	    # 通过此url获取数据，其中带有参数SHOWTYPE、CATALOGID、loading以及random
	    # 但random好像对数据的获取并无影响，因此暂不处理
	    url2 = 'http://www.szse.cn/api/report/ShowReport/data'
	    response2 = requests.get(url=url2, headers=headers,
	        		params={'SHOWTYPE':'JSON', 'CATALOGID':'%s' % catalog_id, 'loading':'first'})
	    html = response2.content.decode('utf-8')
	    # 日期字段
	    date = re.findall(r'"defaultValue":"(.+?)"', html, re.DOTALL)[0]
	    # 列字段，此处有字母简写，也有中文，故而要分别清洗出来
	    cols = re.findall(r'"cols":({.+?})',html,re.DOTALL)[0].replace('<br>','')
	    cols_alp = re.findall(r'"(\w+?)":',cols)
	    cols_hanz = re.findall(r':"(.+?)"',cols)
	    # 行业统计数据
	    data = re.findall(r'"data":\[(.+?)]',html,re.DOTALL)[0]
	    # 清洗数据
	    cleaned_data = re.findall(r'"hymc":"(.+?)","zqsl":"(.+?)","cjje":"(.+?)","cjsl":"(.+?)",'
	                              r'"zgb":"(.+?)","sjzz":"(.+?)","ltgb":"(.+?)","ltsz":"(.+?)"',data)
	    # 这里是将英文字段替换成中文，增加可读性（对实现功能无影响）
	    for i in range(len(cols_hanz)):
	        data = data.replace(cols_alp[i],cols_hanz[i])
	    # 图表的x轴，即各个行业
	    xAxis = []
	    # 成交总额
	    amount = []
	    # 总市值
	    market_cap = []
	    # 流通市值
	    market_equity = []
	    # 从干净的数据中提取出来,筛选感兴趣的行业
	    selected = ['制造业','信息技术','金融业','房地产','科研服务']
	    for item in cleaned_data[:-1]:
	    	if item[0] in selected:
	        	xAxis.append(item[0])
		        amount.append(float(item[2] if ',' not in item[2] else item[2].replace(',','') ))
		        market_cap.append(float(item[5] if ',' not in item[5] else item[5].replace(',','')))
		        market_equity.append(float(item[7] if ',' not in item[7] else item[7].replace(',','')))

	    return xAxis,amount,market_cap,market_equity,date

def get_aphorism():
    import random
    aphorism_list = ['怕什么真理无穷，进一寸有一寸的欢喜。',
                     '君子曰：学不可以已。',
                     '非学无以广才，非志无以成学。',
                     '人生不是追求幸福，而是避免痛苦和无聊。',
                     '今晚夜色真美。',
                     '欲买桂花同载酒，终不似，少年游。',
                     '为天地立心，为生民立命，为继往圣绝学。',
    ]
    return random.choice(aphorism_list)
