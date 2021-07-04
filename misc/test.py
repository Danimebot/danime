import urllib3



for url in urls:
    try:
        urllib3.urlopen(url)
    except urllib3.HTTPError, e:
        
        