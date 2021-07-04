import requests
from bs4  import BeautifulSoup 
import urllib.request
import os
from pybooru import Danbooru
from syncer import sync
import cfscrape
import regex as re
import random

#If multiple tags, add them with +, same things with ratings

def yandere(url):
	urls = []

	payload = {
	'inUserName': 'vein05',
	'inUserPass': 'vein6969'
	}
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
	'From': 'man359905@gmail.com' 
	}
	with requests.Session() as s:
		p = s.post('https://yande.re/user/login', data=payload, headers=headers)
		if url.startswith("https"):
			r = s.get(f'{url}').text
		else:
			page = random.randint(1,100) 
			url1 = f"https://yande.re/post?page={page}?tags={url}"

			r = s.get(url1).text
	
	
	
	try:
		soup = BeautifulSoup(r, "lxml")
		posts_list = soup.find('ul', {'id': 'post-list-posts'})
		posts = posts_list.findAll('li')
		s.close()
	except:
		r = s.get("https://yande.re/post?tags={url}").text
		soup = BeautifulSoup(r, "lxml")
		posts_list = soup.find('ul', {'id': 'post-list-posts'})
		posts = posts_list.findAll('li')
		s.close()

	for post in posts:
		try:
			x = str((post["class"][2]))
			if x == "has-parent":
				continue
		except:
			pass
		url = post.find('a', {'class': 'directlink'})['href']
		if 'https:' not in url:
			url = '{}{}'.format('https:', url)
		if url.endswith("mp4"):
			continue
		if url.endswith("webm"):
			continue
		urls.append(url)
	return urls
def konachan(url):
	urls = []

	payload = {
	'inUserName': 'vein05',
	'inUserPass': 'vein6969'
	}
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
	'From': 'man359905@gmail.com' 
	}
	with requests.Session() as s:
		p = s.post('https://konachan.com/user/login', data=payload, headers= headers)
		if url.startswith("https"):
			r = s.get(f'{url}').text
		else:
			page = random.randint(1, 100)
			url = f"https://konachan.com/post?page={page}?tags={url}"
			r = s.get(url).text		
	s.close()
	soup = BeautifulSoup(r, "lxml")

	posts_list = soup.find('ul', {'id': 'post-list-posts'})
	posts = posts_list.findAll('li')
	for post in posts:
		try:
			x = str((post["class"][2]))
			if x == "has-parent":
				continue
		except:
			pass
		url = post.find('a', {'class': 'directlink'})['href']
		if 'https:' not in url:
			url = '{}{}'.format('https:', url)
		if url.endswith("mp4"):
			continue
		if url.endswith("webm"):
			continue
		urls.append(url)
	return urls


def danbooru(tags = None, page = None):
	tags = tags.replace(";", "_")
	tags = tags.replace("+", " ")
	urls = []
	client = Danbooru('danbooru', username='vein05', api_key='eq2Fpf3UAUC2K796k82pXEsm')
	posts = client.post_list(tags=tags, page = page, limit = 100)
	if page == None:
		page = 1
	
	for post in posts:

		if post['parent_id'] != None:
			continue
		try: 
			url = post['file_url']
			if url.endswith("webm"):
				continue
			elif url.endswith(".mp4"):
				continue
		except:
			continue
		urls.append(url)
	return urls


# def _3dbooru(tag=None, page= None):
# 			tags = tag.replace("+", " ")
# 			headers = {
# 			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
# 			'From': 'man359905@gmail.com' 
# 			}
# 	# if page == None:
# 		# try:
# 			page = random.randint(1, 50)
# 			url = f"http://behoimi.org/post/index.json?page={page}?tags={tags}"

# 			r = requests.get(url=url, headers= headers).json()
# 			n = 0
# 			for value in r:
# 				url = r[n]
# 				print(url)
# 				n += 1
# 				break
# 		# except:
# 		# 	url = f"http://behoimi.org/post/index.json?tags={tags}"
# 		# 	r =requests.get(url).json()
# 		# 	print(r)
# 	# else:
# 	# 	pass

def safebooru(tags= None, page= None):
	tags = tags.replace(";", "_")
	tags = tags.replace("+", " ")	
	client= Danbooru('safebooru', username='vein05', api_key='eq2Fpf3UAUC2K796k82pXEsm')
	if page == None:
		page = 1
	posts = client.post_list(tags=tags, page=page, limit =100)
	urls = []
	for post in posts:

		if post['parent_id'] != None:
			continue
		try: 
			url = post['file_url']
			if url.endswith("webm"):
				continue
			elif url.endswith(".mp4"):
				continue
		except:
			continue
		urls.append(url)
	return urls

