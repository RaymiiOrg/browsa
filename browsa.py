#!/usr/bin/env python2.7
from bs4 import BeautifulSoup
import sys, urllib2, os, re, random

fallback_url = "http://news.google.com"

try:
    page_url = sys.argv[1]
except IndexError:
    sys.exit("Please provide an URL")

urls = []

try:
    page = urllib2.urlopen(page_url).read()
except Exception:
    page = urllib2.urlopen(fallback_url).read()
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
    url = random.choice(urls)
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
