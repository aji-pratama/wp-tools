import bs4
import lxml
from xml.etree import ElementTree
from bs4 import BeautifulSoup as bs

import os
import urllib.request
from urllib.parse import urlparse

xml_file_name = sys.argv[1]
content = []

with open(xml_file_name, "r") as file:
    content = file.readlines()
    content = "".join(content)
    bs_content = bs(content, 'html.parser')
    items = bs_content.findAll('item')

def download_image(url_req, undownloaded_img=[]):
    try:
        path = '.{}'.format(urlparse(url_req).path)        
        url_ascii = '{}://{}/{}'.format(urlparse(url_req).scheme, urlparse(url_req).netloc, urllib.parse.quote(urlparse(url_req).path))

        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(url_ascii, path)
    except Exception as e:
        undownloaded_img.append({
            "url": url_req,
            "error": e
        })
        print('url: {}, err: {}'.format(url_req, e))
        
def parse_data(items):
    data_blog = []
    for item in items:
        prt_id = item.find('wp:post_parent').get_text()
        data_ = {
            "post_parent": item.find('wp:post_parent').get_text(),
            "asset_url": item.find('wp:attachment_url').get_text(),
        }
        data_blog.append(data_)

    return data_blog


undownloaded_img = []

for data in parse_data(items):
    asset_url = data['asset_url']
    print(asset_url)
    download_image(asset_url, undownloaded_img)
