#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys, urllib2, os, re, random

fallback_urls = [u"https://news.ycombinator.com/", u"http://news.google.com", u"http://raymii.org/s/tags", 
                 u"http://tweakers.net/nieuws", u"http://stackoverflow.com", u"http://reddit.com"]
fallback_url = random.choice(fallback_urls)

try:
    page_url = u"".join(sys.argv[1])
except IndexError:
    sys.exit("Please provide an URL")

urls = []
non_wanted_urls = ['.pdf', '@', '#', '.js', '.jpg', '.png', '.gif']

print(page_url)

page_request = urllib2.Request(page_url)
fallback_request = urllib2.Request(fallback_url)
 
page_request.add_header('User-agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)')
fallback_request.add_header('User-agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)')
page_request.add_header('Accept', 'text/plain')
fallback_request.add_header('Accept', 'text/plain')
page_request.add_header('Accept-Encoding', 'none')
fallback_request.add_header('Accept-Encoding', 'none')

try:
    page = urllib2.urlopen(page_request).read()
except Exception as error:
    page = urllib2.urlopen(fallback_request).read()
    print("# Error in opening URL: %s" % error)

soup = BeautifulSoup(page)

for link in soup.find_all('a'):
    if link.get('href'):
        if re.search("htt(p|ps)\:\/\/", link.get('href').encode('utf-8')):
            urls.append(link.get('href'))

if len(urls) == 0:
    print("# Error: No URLs in list.")
    urls.append(fallback_url)

url = random.choice(urls)

if url == page_url and not page_url == fallback_url:
    url = fallback_url

for item in non_wanted_urls:
    if re.search(item, url):
        url = fallback_url

scriptname = u''.join(sys.argv[0])

command = scriptname + " '" + url + "' &"

try:
    os.system(command)
except Exception as error:
    url = random.choice(urls)
    command = scriptname + " '" + url + "' &"
    os.system(command)

sys.exit()
