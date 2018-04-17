#encoding:utf-8

import re
import io
import string
import sys
import os
import colorama as ca
import urllib
from bs4 import BeautifulSoup
import requests
from lxml import etree
import lxml.html.soupparser as soupparser

# 更换代理获取地址为http://www.xicidaili.com/wt/

# 目标文件名
tarFileName = 'proxies.pkt'

ca.init(autoreset=True)
timeout = 1


# 获取代理地址页面, 从5页中筛选出存活时间一天以上，且速度最快的25个
def main():
	proxy_dic_list = []
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}	
	for page in range(1,5):
		url = 'http://www.xicidaili.com/wt/%d'%page
		requ = requests.get(url,headers= header)
		lxml = requ.content
		selector = etree.HTML(lxml)
		page_content = selector.xpath('//tr')[1:]
		for index, p in enumerate(page_content):
			tds = p.xpath('td')
			proxy_dic = {}
			proxy_dic['ip']   = str(tds[1].text)
			proxy_dic['port'] = str(tds[2].text)
			proxy_dic['life'] = str(tds[8].text)
			proxy_dic_list.append(proxy_dic)
		print(ca.Back.BLUE + "Page %d is Done"%page)
	count = 0
	valid_proxy_list = []
	for proxy in proxy_dic_list:
		if proxy['life'].find('天') != -1:
			# print(ca.Back.BLUE + proxy['ip'] + ":"+proxy['port'] + " " + proxy['life'])
			# 检查
			isValid, time = checkProxy(count, proxy['ip'] + ":"+proxy['port'])
			if isValid:
				valid_dic = proxy
				valid_dic['time'] = time
				valid_proxy_list.append(valid_dic)
			count += 1
	# 二次筛选
	print(ca.Back.YELLOW + "\nSecondary Check Start")
	second_count = 0
	second_valid_proxy_list = []
	for proxy in valid_proxy_list:
		isValid, time = checkProxy(second_count, proxy['ip'] + ":"+proxy['port'])
		if isValid:
			valid_dic = proxy
			valid_dic['time'] = time
			second_valid_proxy_list.append(valid_dic)
		second_count += 1

	writeFile(second_valid_proxy_list)

#检查代理的延迟等	
def checkProxy(index, proxy):
	try:
		tempdic = {}
		tempdic['http'] = 'http://' + proxy
		url = 'http://115.182.34.168'
		req = requests.get(url,timeout=timeout,proxies = tempdic)
		# req = requests.get(r'http://' + proxy,timeout = timeout)
		time = req.elapsed.microseconds
		print(ca.Fore.GREEN + str(index)+' : ' + proxy + ' is OK! timeout = %d ms'%time)
		# print str(index)+' : ' + proxy + ' is OK! timeout = %d ms'%time
		return True, time
	except Exception as e:
		print(ca.Fore.RED + str(index)+' : ' +proxy + ' is failed!')
		# print(e)
		# print str(index)+' : ' +proxy + ' is failed!'	
		return False, 9999999

# 写入pickle
# 格式为
# [{'http':'192.168.1.1:8000'},]
import pickle
def writeFile(dic_list):	
	output = []		
	dic_list = sorted(dic_list,key = lambda dic_list: dic_list['time'])
	if len(dic_list) < 25:
		diclen = len(dic_list)
	else:
		diclen = 25

	for index,item in enumerate(dic_list[:diclen]):#选取延迟最小
		out_dic = {}
		out_dic['http'] = item['ip'] + ":"+item['port']
		output.append(out_dic)
	print(output)
	# 写新文件
	out_file = open(tarFileName,'wb')
	pickle.dump(output, out_file, -1)
	out_file.close()
	print('Done!')
			
# print checkProxy(1,'117.177.250.151:8080')
main()
# writeFile()
