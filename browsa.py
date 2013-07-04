#!/usr/bin/env python2.7
from bs4 import BeautifulSoup
import sys, urllib2, os, re, random

fallback_url = "http://news.google.com"

try:
    page_url = sys.argv[1]
except IndexError:
    sys.exit("Please provide an URL")

urls = []

page_request = urllib2.Request(page_url)
fallback_request = urllib2.Request(fallback_url)
 
page_request.add_header('User-agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)')
fallback_request.add_header('User-agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)')
page_request.add_header('Accept', 'text/plain')
fallback_request.add_header('Accept', 'text/plain')
  
try:
    page = urllib2.urlopen(page_request).read()
except Exception:
    page = urllib2.urlopen(fallback_request).read()
    print("---")
soup = BeautifulSoup(page)
for link in soup.find_all('a'):
    if re.search("htt(p|ps)\:\/\/", str(link.get('href'))):
        # print(link.get('href'))
        urls.append(link.get('href'))
    else:
        if link.get('href'):
            # print(str(page_url) + str(link.get('href')))
            urls.append(str(page_url) + str(link.get('href')))
if len(urls) == 0:
    print("----")
    urls.append(fallback_url)
url = random.choice(urls)

if url == page_url:
    sys.exit()
if re.search("@", url) or re.search("#", url):
    sys.exit()

scriptname = sys.argv[0]

command = scriptname + " '" + url + "' &"
print(url)

try:
    os.system(command)
except Exception as error:
    url = random.choice(urls)
    command = scriptname + " '" + url + "' &"
    os.system(command)

sys.exit()
