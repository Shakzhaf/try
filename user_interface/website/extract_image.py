from urllib.request import urlopen
#import urllib.request as Request
import urllib
from bs4 import BeautifulSoup
import re
import concurrent.futures

def get_image(url, number_of_images=1):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    #req = urllib.request(url, headers=hdr)
    #page = urllib.urlopen(req)
    
    
    request = urllib.request.Request(url, headers=hdr)
    opener = urllib.request.build_opener()
    response = opener.open(request)
    bs = BeautifulSoup(response, 'html.parser')
    
    image = bs.find_all('img', {'src':re.compile('.jpg')})
    if len(image)<1:
        image.append({'src':'http://netdna.webdesignerdepot.com/uploads/2008/11/sample-graphic.jpg'})
    return image[0]['src']

def get_images(links):
    images=[]
    for url in links:
        images.append(get_image(url))
    return images

def get_images_concurrently(img_urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results=executor.map(get_image, img_urls)
    return(list(results))

    #url='https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/7'
    #images=get_image(url)
    #print(images)

