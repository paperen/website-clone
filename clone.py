#!/usr/bin/env
# -*- coding: UTF-8 -*-
#Filename: clone.py

import urllib,re,time,sys,core,webbrowser,getopt,os

def usage():
	print u'''
 -h or --help 说明
 -u or --url 站点网址(site url)
 -d or --dir [可选]保存本地目录，默认为站点域名(which directory to save files[option])
 例子(example):
  py clone.py -u paperen.com
  clone -u paperen.com -d test (windows下)
'''
	return 0

def show_progress():
	sys.stdout.write("=")
	time.sleep(0.1)

def main():
	url = ""
	root = None
	try :
		opts,args = getopt.getopt(sys.argv[1:], 'u:d:h:',
		    [
			'url=',
			'dir=',
			'help=',
			] 
		)
		for opt, val in opts:
			if opt in ( '-u', '--url' ):
				url = val
			elif opt in ( '-d', '--dir' ):
				root = val
			elif opt in ( '-h', '--help' ):
				usage()
			else:
				raise Exception
	except getopt.GetoptError, err:
		usage()

	try :
		if root != None and os.path.exists(root) == False:
			print u"保存路径不存在，请先创建该目录(directory not exists)";

			raise Exception
		if len(url) == 0:
			print u"输入的网址有误(url invalid)或查看帮助 -h";
			raise Exception

		if url.find('http://') == -1: url = 'http://' + url
		url_list = url.replace('http://', '').split('/')

		# 获取域名
		if url_list[0] == 'localhost':
			domain = url.replace('http://', '').strip('/')
		else:
			domain = url_list[0]
		if domain == '':
			print u"输入的网址有误(url invalid)";
			raise Exception

		t = core.thief(domain,root)

		# 爬取网页
		opener = urllib.FancyURLopener({})
		f = opener.open(url)
		html = f.read()
		if len(html) == 0 :
			print u"获取网页失败(url fetch error)"
			raise Exception

		# css
		# <link href="http://paperen.com/theme/paperen/bootstrap.css" rel="stylesheet" />
		# <link rel="stylesheet" type="text/css" href="http://events.hytera.com/theme/hytera/common.css" media="all" />
		# <link href="http://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet" />
		sys.stdout.write( u"开始爬取css" )
		css = re.findall(r"<\s*link\s+[^>]*href\s*=\s*[\"|\'](.*?)[\"|\'][^>]+[\s\S]*?>", html)
		total = len(css)
		for v in css:
			if (v.find('http://') == -1 and v.find(domain) != -1) or v.find('.css') != -1:
				html = html.replace(v,t.get(v))
			show_progress()
		sys.stdout.flush()
		print u"爬取css完成"

		# js
		# <script src="http://paperen.com/js/jquery-1.7.1.min.js"></script>
		# <script src="/js/jquery-1.7.1.min.js"></script>
		# <script src="http://fonts.googleapis.com/js/jquery-1.7.1.min.js"></script>
		sys.stdout.write( u"开始爬取js" )
		js = re.findall(r"<\s*script\s+[^>]*?src\s*=\s*[\"|\'](.*?)[\"|\'][\s\S]*?>", html)
		total = len(js)
		for v in js:
			if (v.find('http://') == -1 or v.find(domain) != -1) and v.find('.js') != -1:
				html = html.replace(v,t.get(v))
			show_progress()
		sys.stdout.flush()
		print u"爬取js完成"


		# image
		# <img src="http://paperen.com/file/182" alt="http://paperen.com/file/182" />
		# <img src="http://events.hytera.com/upload/2016/03/22/62150172eebd2d423c42cdc511446bd7.jpg" class="dpb main-banner-img">
		# <img src="/upload/2016/03/22/62150172eebd2d423c42cdc511446bd7.jpg" class="dpb main-banner-img">
		sys.stdout.write( u"开始爬取图片" )
		img = re.findall(r"<\s*img\s+[^>]*?src\s*=\s*[\"|\'](.*?)[\"|\'][\s\S]*?>", html)
		pattern_img = re.compile(".*\.[jpg|jpeg|gif|png|bmp]")
		total = len(img)
		for v in img:
			if (v.find('http://') == -1 or v.find(domain) != -1) and pattern_img.match(v) != None:
				html = html.replace(v,t.get(v))
			show_progress()
		sys.stdout.flush()
		print u"爬取图片完成"


		# 保存网页
		index = t.getroot()+'index.html'
		fp = open(index, 'wb')
		fp.write(html)
		fp.close()
		print u"生成页面完成，请打开 " + index + u" 查看效果"

		# 打开网页
		webbrowser.open(index, 2, True)

	except Exception:
		print u"爬取失败"

if __name__ == "__main__":
    main()