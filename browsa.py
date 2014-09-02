#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys, urllib2, os, re, random

fallback_urls = [u"https://news.ycombinator.com/", u"http://news.google.com", u"http://raymii.org/s/tags", 
                 u"http://tweakers.net/nieuws", u"http://stackoverflow.com", u"http://reddit.com"]

def get_url(page_url) :

    global fallback_urls
    fallback_url = random.choice(fallback_urls)

    print("URL: " + page_url)
    
    page_request = urllib2.Request(page_url)
    fallback_request = urllib2.Request(fallback_url)
     
    page_request.add_header('User-agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)')
    fallback_request.add_header('User-agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)')
    page_request.add_header('Accept', 'text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    fallback_request.add_header('Accept', 'text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    page_request.add_header('Accept-Encoding', 'none')
    fallback_request.add_header('Accept-Encoding', 'none')
    page_request.add_header('DNT', '1')
    fallback_request.add_header('DNT', '1')
    page_request.add_header('Connection', 'keep-alive')
    fallback_request.add_header('Connection', 'keep-alive')
    
    try:
        page = urllib2.urlopen(page_request).read()
        fallback_urls.append(page_url)
    except Exception as error:
        try:
            page = urllib2.urlopen(fallback_request).read()
            print("# Error in opening URL: %s. Falling back to fallback url: %s" % (error, fallback_url))
        except Exception as error:
            print("# Fallback URL %s also failed with error: %s. Giving up." % (fallback_url, error))
            print("# Fallback URL's collected: ")
            for url in fallback_urls:
                print("# %s" % url)
            print("")
            sys.exit(1)

    soup = BeautifulSoup(page)
    return soup
    
def get_all_links_from_soup(soup):
    urls = []
    for link in soup.find_all('a'):
        if link.get('href'):
            if re.search("htt(p|ps)\:\/\/", link.get('href').encode('utf-8')):
                urls.append(link.get('href'))
    print("%i URL's on page" % len(urls))
    return urls

def choose_new_url(urls, previous_url):
    global fallback_urls
    fallback_url = random.choice(fallback_urls)
    non_wanted_urls = ['.pdf', '@', '#', '.js', '.jpg', '.png', '.gif']
    
    if len(urls) == 0:
        print("# Error: No URLs in list.")
        urls.append(fallback_url)
     
    url = random.choice(urls)
    print("Contemplating random URL: %s" % url) 
    
    if url == previous_url:
        print("# New URL Would be the same as previous URL")
        if not fallback_url == previous_url:
            print("# Choosing a fallback URL.")
            url = fallback_url
        else:
            print("# Previous URL is also the fallback URL.")
            url = fallback_url

    
    for item in non_wanted_urls:
        if re.search(item, url):
            print("# Part of the new URL is on the non wanted list. Choosing fallback URL.")
            url = fallback_url

    print("New URL: %s" % url) 
    return url


def launch_myself_in_background(url):
    scriptname = u''.join(sys.argv[0])
    
    command = scriptname + " '" + url + "' &"
    
    try:
        os.system(command)
    except Exception as error:
        url = random.choice(urls)
        command = scriptname + " '" + url + "' &"
        os.system(command)
    
    sys.exit()

def the_magic(url):
    soup = get_url(url)
    urls = get_all_links_from_soup(soup)
    new_url = choose_new_url(urls, url)
    return new_url

def main():
    try:
        page_url = u"".join(sys.argv[1])
    except IndexError:
        sys.exit("Please provide an URL")

    while True:
        page_url = the_magic(page_url)
    print("")
    
if __name__ == "__main__":
    main()
