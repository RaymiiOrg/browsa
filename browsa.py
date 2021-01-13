#!/usr/bin/env python3
# author: Remy van Elst - https://raymii.org
# license: gnu agpl v3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys, urllib.request, urllib.error, urllib.parse, os, re, random, time

fallback_urls = ["http://news.google.com", "https://hackurls.com/", "https://nu.nl", "http://raymii.org/s/everything.html"]
previous_urls = [""]

counter = 0

def dedup_list(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


def log(line):
    print(line)
    with open("browsa.log", "a+") as log_file:
        log_file.write("%s \n" % str(line))

def get_url(page_url) :

    global fallback_urls
    fallback_url = random.choice(fallback_urls)

    log("# Info: Downloading URL: %s" % page_url)
    
    page_request = urllib.request.Request(page_url)
    fallback_request = urllib.request.Request(fallback_url)

     
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
        page = urllib.request.urlopen(page_request, timeout=5).read()
        fallback_urls.append(page_url)
    except Exception as error:
        try:
            page = urllib.request.urlopen(fallback_request, timeout=5).read()
            log("# Error: opening URL: %s failed. Falling back to fallback url: %s" % (error, fallback_url)) 
        except Exception as error:
            log("# Error: Fallback URL %s also failed with error: %s. Giving up." % (fallback_url, error))
            log("# Error: Fallback URL's collected: ")
            for url in fallback_urls:
                log("# Error: %s" % url)
            log("")
            sys.exit(1)

    soup = BeautifulSoup(page, features="lxml")
    return soup
    
def get_all_links_from_soup(soup):
    urls = []
    for link in soup.find_all('a'):
        if link.get('href'):
            if re.search("htt(p|ps)\:\/\/", link.get('href').encode('utf-8')):
                urls.append(link.get('href'))
    log("# Info: URL's on page: %s" % len(urls))
    return urls

def choose_new_url(urls, previous_url):
    global fallback_urls
    global previous_urls
    dedup_list(fallback_urls)
    dedup_list(previous_urls)
    previous_urls = previous_urls[:5]
    previous_urls.append(previous_url)
    fallback_url = random.choice(fallback_urls)
    non_wanted_urls = ['.pdf', '@', '#', '.js', '.jpg', '.png', '.gif']
    
    if len(urls) == 0:
        log("# Error: No URLs in list.")
        urls.append(fallback_url)
     
    new_url = random.choice(urls)
    log("# Info: New URL: %s" % new_url) 
    
    if new_url in previous_urls[:5]:
        log("# Error: New URL Would be the same as previous URL")
        if not fallback_url in previous_urls[:5]:
            log("# Error: Choosing a fallback URL.")
            new_url = fallback_url
        else:
            log("# Error: Previous URL is also the fallback URL.")
            new_url = fallback_url

    
    for item in non_wanted_urls:
        match = re.search(item, new_url)
        if match:
            log("# Error: Part of the new URL is on the non wanted list: %s. Choosing fallback URL." % match.group())
            new_url = fallback_url

    previous_urls.append(new_url)
    return new_url

def launch_myself_in_background(url):
    scriptname = ''.join(sys.argv[0])
    command = scriptname + " '" + url + "' &"
    
    try:
        os.system(command)
    except Exception as error:
        url = random.choice(urls)
        command = scriptname + " '" + url + "' &"
        os.system(command)
    
    sys.exit()

def the_magic(url):
    global counter
    counter += 1
    log("# Info: Count %i" % counter)
    soup = get_url(url)
    urls = get_all_links_from_soup(soup)
    new_url = choose_new_url(urls, url)
    return new_url

def main():
    try:
        page_url = "".join(sys.argv[1])
    except IndexError:
        sys.exit("Please provide an URL")

    while True:
        page_url = the_magic(page_url)
    # time.sleep(5)
    log("")
    
if __name__ == "__main__":
    main()
