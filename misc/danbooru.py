from pybooru import Danbooru
from random import randint
import urllib.request



def download(tags, pages):
    x = []  # link storage
    try:
        client = Danbooru('danbooru', username='vein05', api_key='eq2Fpf3UAUC2K796k82pXEsm')
        a= 0
        if a == 0:
            randompage = randint(1, pages)
            posts = client.post_list(tags=tags, page=randompage, limit=200)
            z = 0
            for post in posts:
                try:
                    fileurl = post['file_url']
                except:
                    fileurl = 'https://danbooru.donmai.us' + post['source']
                x.append(fileurl)
                if z== 199:
                    break
                z+=1

    except Exception as e:
        raise e
    return x 
