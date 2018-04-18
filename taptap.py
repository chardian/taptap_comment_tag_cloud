# -*- coding: utf-8 -*-
"""

"""
import random
import sys
import time

import requests
from bs4 import BeautifulSoup
from pytagcloud import create_tag_image, make_tags, LAYOUT_HORIZONTAL
from pytagcloud.colors import COLOR_SCHEMES


class HttpTool(object):
	HEADER_POOL = [
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
		"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
		"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

	@staticmethod
	def get_random_headers():
		header = {'User-Agent': random.choice(HttpTool.HEADER_POOL)}
		print header
		return header


class TapTap(object):
	def __init__(self, url, page_range, game_name):
		self.__url = url
		self.__page_range = page_range
		self.__html_file_name = game_name + '_html.txt'
		self.__comment_file_name = game_name + '_comment.txt'
		self.__tag_image_file_name = game_name + '_tag.png'
		self.__game_name = game_name

	def __call__(self, *args, **kwargs):
		for page in self.__page_range:
			self.__store_page_data(page)
		self.__resolve_page_data()
		self.__generate_tag_cloud()
		#self.__check_info_reference('氪金')

	def __store_page_data(self, page):
		page_url = self.__url.format(page)
		page_request = requests.get(page_url, headers=HttpTool.get_random_headers(), timeout=30)
		page_request.encoding = 'GBK'
		page_text = page_request.content
		with open(self.__html_file_name, 'a') as file:
			file.write(page_text)
			file.flush()
			file.close()

	def __resolve_page_data(self):
		with open(self.__html_file_name, 'r') as file:
			soup = BeautifulSoup(file, 'html.parser', from_encoding='gb18030')
			comments_div = soup.find_all('div', class_='item-text-body')
			comments = [div.text for div in comments_div]
			comment_file = open(self.__comment_file_name, 'a')
			comment_file.writelines(comments)
			comment_file.flush()
			comment_file.close()

	def __generate_tag_cloud(self):
		import jieba.analyse
		jieba.add_word('氪金')
		jieba.add_word('逼氪')
		jieba.add_word('骗氪')
		jieba.add_word('王者荣耀')
		jieba.del_word('...')
		jieba.del_word('只能')
		jieba.del_word('可能')
		jieba.del_word('觉得')
		jieba.del_word('而且')
		jieba.del_word('然后')
		jieba.del_word('还有')
		jieba.del_word('游戏')

		comments_file = open(self.__comment_file_name, 'r')
		tags = jieba.analyse.extract_tags(comments_file.read(), topK=100, withWeight=True)
		comments_file.close()
		dd = []
		for i in tags:
			dd.append((i[0], int(float(i[1] * 1000))))
			print 'i is ', i[0], i[1]
		tags = make_tags(dd, minsize=10, maxsize=80, colors=COLOR_SCHEMES['audacity'])
		create_tag_image(
			tags,
			self.__tag_image_file_name,
			size=(600, 600),
			layout=LAYOUT_HORIZONTAL,
			fontname='SimHei'  #  !!! 注意字体需要自己设置了才会有效, 见ReadMe
		)
		print self.__tag_image_file_name

	def __check_info_reference(self, key_word):
		"""输出所有提到key_word的玩家给出的所有评论以及平均分"""
		print type(key_word)
		result_file_name = (self.__game_name + '_' + key_word + '.txt').decode('utf-8').encode('gbk')
		with open(self.__html_file_name, 'r') as file:
			soup = BeautifulSoup(file, 'html.parser', from_encoding='gb18030')
			review_li = soup.find_all('li', class_='taptap-review-item collapse in')
			result_file = open(result_file_name,'w')
			total_score = 0
			total_people = 0
			for li in review_li:
				comment = li.find('div', class_='item-text-body').text
				if key_word in comment:
					score = int(li.find('i', class_='colored').attrs['style'][-4:-2]) / 14
					total_score += score
					total_people += 1
					comment_time = int(li.find('a', class_='text-header-time').span.attrs['data-dynamic-time'])
					result_file.write('评论:' + comment + '\n')
					result_file.write('评分' + str(score) + '星 \n')
					result_file.write('时间' + (time.strftime('%m-%d %H:%M:%S', time.localtime(comment_time))) + '\n')
					result_file.flush()
			star_score = float(total_score) / float(total_people)
			average_score = 2 * star_score
			result_file.write('总评论数' + str(len(review_li)) + '\n')
			result_file.write('相关评论次数' + str(total_people) + '\n')
			result_file.write('平均分是' + str(average_score) + '\n')
			result_file.write('平均星数' + str(star_score) + '\n')
			result_file.flush()
			result_file.close()

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	url = 'https://www.taptap.com/app/68681/review?order=update&page={}#review-list'
	game_name = 'qwq'
	page_range = range(1, 20)
	obj = TapTap(url, page_range, game_name)
	obj(*sys.argv)
