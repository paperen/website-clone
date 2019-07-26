#!/usr/bin/env
#-*- coding: UTF-8 -*-
#Filename: thief.py

import os,sys,urllib,re

class thief:
	_url = ""
	_root = ""
	_siteurl = ""
	def __init__(self,u,r):
		self._op = urllib.FancyURLopener({})
		self._url = u
		# 拼接根目录
		url_list = u.split('/')
		self._siteurl = url_list[0] + '//' + url_list[2]
		print self._url
		if  r == None :
			self._root = sys.path[0] + os.path.sep + url_list[2]+os.path.sep
		else :
			self._root = r+os.path.sep
		self.create_dir(self._root,True)

	# 爬取文件 & 建立目录
	def get(self,something):
		something = something.replace(self._siteurl, '')
		# print something
		if re.search(r"^((https://|http://|//)+)[^\s]+",something) != None:
			# print '远程地址不处理'
			return something
		d = self.create_dir(something,False)
		if d[1] != '' and d[1] != None:
			data = self.read(something)
			self.save(data,d[0]+d[1])

			# 判断是否是CSS
			if d[1].split('.').pop() == 'css':
				self.parse_css(something,data)

		return something.replace(self._siteurl, '').strip('/')

	# [返回本地文件夹路径,文件名]
	def create_dir(self,d,is_root):
		if is_root:
			t = d
			f = None
		else:
			t = d.strip('/').split('/')
			f = t.pop()
			f_list = re.findall(r"^(.*?)[\?|\#].*", f)
			if f_list != [] : f = f_list[0]
			t = "/".join(t)
			t = self._root + t.replace('/', os.path.sep)
		if os.path.exists(t) == False :
			os.makedirs(t)
		return [t + os.path.sep,f]

	def read(self,url):
		if url.find(self._siteurl) == -1:
			# 根目录拼接
			if url.find('/') == 0:
				url = self._siteurl+'/'+url
			# 相对路径拼接
			else:
				url = os.path.dirname(self._url)+'/'+url
		f = self._op.open(url)
		return f.read()

	def save(self,data,filename):
		fp = open(filename, 'wb')
		fp.write(data)
		fp.close()

	def getroot(self):
		return self._root

	def parse_css(self,url,data):
		t = url.split('/')
		t.pop()
		url = "/".join(t)+'/'
		img = re.findall(r"url\((.*?)\)", data)
		for v in img:
			if v.find('data:') == -1 : self.get(url+v.strip('\''))
		 
