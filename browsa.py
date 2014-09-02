#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys, urllib2, os, re, random, time

fallback_urls = [u"https://news.ycombinator.com/", u"http://news.google.nl", u"http://raymii.org/s/tags", 
                 u"http://www.nu.nl/", u"http://buienradar.nl/", u"http://www.marktplaats.nl/",
                 u"http://www.bol.com/", u"http://www.ah.nl/", u"https://www.pinterest.com/",
                 u"http://www.geenstijl.nl/", u"http://www.dumpert.nl/", u"http://www.ad.nl/",
                 u"http://nos.nl/", u"http://www.funda.nl/", u"http://frontpage.fok.nl/",
                 u"http://9gag.com/", u"http://www.nrc.nl/", u"http://www.zalando.nl/",
                 u"http://tweakers.net/nieuws", u"http://stackoverflow.com", u"http://reddit.com"]

def log(line):
    print(line)
    with open("browsa.log", "a+") as log_file:
        log_file.write(line)

def get_url(page_url) :

    global fallback_urls
    fallback_url = random.choice(fallback_urls)

    log("Downloading URL: %s" % page_url)
    
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
            log("# Error in opening URL: %s. Falling back to fallback url: %s" % (error, fallback_url))
        except Exception as error:
            log("# Fallback URL %s also failed with error: %s. Giving up." % (fallback_url, error))
            log("# Fallback URL's collected: ")
            for url in fallback_urls:
                log("# %s" % url)
            log("")
            sys.exit(1)

    soup = BeautifulSoup(page)
    return soup
    
def get_all_links_from_soup(soup):
    urls = []
    for link in soup.find_all('a'):
        if link.get('href'):
            if re.search("htt(p|ps)\:\/\/", link.get('href').encode('utf-8')):
                urls.append(link.get('href'))
    log("URL's on page: %s" % len(urls))
    return urls

def choose_new_url(urls, previous_url):
    global fallback_urls
    fallback_url = random.choice(fallback_urls)
    non_wanted_urls = ['.pdf', '@', '#', '.js', '.jpg', '.png', '.gif']
    
    if len(urls) == 0:
        log("# Error: No URLs in list.")
        urls.append(fallback_url)
     
    new_url = random.choice(urls)
    log("New URL: %s" % new_url) 
    
    if new_url == previous_url:
        log("# New URL Would be the same as previous URL")
        if not fallback_url == previous_url:
            log("# Choosing a fallback URL.")
            new_url = fallback_url
        else:
            log("# Previous URL is also the fallback URL.")
            new_url = fallback_url

    
    for item in non_wanted_urls:
        match = re.search(item, new_url)
        if match:
            log("# Part of the new URL is on the non wanted list: %s. Choosing fallback URL." % match.group())
            new_url = fallback_url

    return new_url


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
    log("")
        time.sleep(5)
    
if __name__ == "__main__":
    main()
