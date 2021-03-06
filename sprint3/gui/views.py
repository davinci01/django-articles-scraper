# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.shortcuts import render
from .models import articles
from bs4 import BeautifulSoup as bf
import requests, cfscrape, sys, time

articles.objects.all().delete()

def get_proxies():
    # Find a free proxy provider website
    # Scrape the proxies
    proxy_web_site = 'https://free-proxy-list.net/'
    response = requests.get(proxy_web_site)
    page_html = response.text
    page_soup = bf(page_html, "html.parser")
    containers = page_soup.find_all("div", {"class": "table-responsive"})[0]
    ip_index = [8 * k for k in range(80)]
    proxies = set()

    for i in ip_index:
        ip = containers.find_all("td")[i].text
        port = containers.find_all("td")[i + 1].text
        https = containers.find_all("td")[i + 6].text
        print("\nip address : {}".format(ip))
        print("port : {}".format(port))
        print("https : {}".format(https))

        if https == 'yes':
            proxy = ip + ':' + port
            proxies.add(proxy)

    return proxies


def check_proxies():

    # check the proxies and save the working ones

    proxies = get_proxies()
    test_url = 'https://httpbin.org/ip'
    for i in proxies:
        print("\nTrying to connect with proxy: {}".format(i))
        try:
            response = requests.get(test_url, proxies={"http": i, "https": i}, timeout=5)
            print("working proxy found")
            return i
            break
        except:
            print("Connnection error")
    return 0

def category(text, knum):

    #   open keyword files

    try:
        sport = open("sport.csv", "r")
        health = open("health.csv", "r")
        science = open("science.csv", "r")
    except:
        print("keywords files not found (sport.csv , health.csv, science.csv)")
        sys.exit(1)
    index = "None"
    i, j, h = 0, 0, 0

    #   check if keyword in article body or title

    for keyword in sport:
        keyword = keyword.strip().lower()
        if keyword in text.lower():
            i = i + 1
    for keyword in health:
        keyword = keyword.strip().lower()
        if keyword in text.lower():
            j = j + 1
    for keyword in science:
        keyword = keyword.strip().lower()
        if keyword in text.lower():
            h = h + 1

    #   check the if keywords exist in article are more then the variable knum

    if max(i, j, h) == i and i > knum:
        index = "sport"
    elif max(i, j, h) == j and j > knum:
        index = "health"
    elif max(i, j, h) == h and h > knum:
        index = "science"

    #   close keywords files

    sport.close()
    health.close()
    science.close()

    #   return the category of article

    return index
elwatan_freq=240
def scraper2():
    c=0
    try:
        r2 = requests.get("https://www.elwatan.com/edition/actualite")
        unicode_str2 = r2.content.decode('utf8')
        encoded_str2 = unicode_str2.encode("utf-8")
    except:
        print("request failed try again")
        return
    if r2.status_code == 200:
    	array = []
        soup = bf(encoded_str2, "html.parser")
        title = soup.find_all('h3', {'class': 'title-14'})
        img = soup.find_all('article' , {'class':'post post-tp-24'})
        for i in img:
            im = bf(str(i), "html.parser")
            try:
                im = im.find_all('img')
                im = im[0]["src"]
                array.append(im)
            except:
                array.append("https://i.ibb.co/8cfP6ZD/elwatan.png")
        for i in title:
            link = bf(str(i), "html.parser")
            link = link.find_all('a')
            link = link[0]["href"]
            articles(title=i.get_text().encode("utf-8"),link=link,img=array[c],category=category(str(i.get_text().encode("utf-8")),0)).save()
            c=c+1
def scraper1():

    #   send request and encode results

    try:
        r1 = requests.get("https://www.liberte-algerie.com/actualite")
        unicode_str1 = r1.content.decode('utf8')
        encoded_str1 = unicode_str1.encode("utf-8")
    except:
        print("no working proxy found")
        return


    if r1.status_code == 200:

        #   create beautiful soup object

        soup = bf(encoded_str1, "html.parser")

        #   get article title

        title = soup.find_all('a', {'class': 'title'})
        mg = soup.find_all('div', {'class': 'span-8'})
        img = mg[0].find_all('li')
        array = []
        co = 0
        for i in img:
            im = bf(str(i), "html.parser")
            try:
                im = im.find_all('img')
                im = im[0]["src"]
                array.append(im)
            except:
                array.append("https://i.ibb.co/fDDLYQc/libre.jpg")
        c = 0

        #   create tables to save articles1

        for i in title:

            #   get link and article as text

            link = title[c]['href']
            articles(title=i.get_text().encode("utf-8").strip(),link="https://www.liberte-algerie.com"+link,img=array[c],category=category(str(i.get_text().encode("utf-8")),0)).save()
            c = c + 1
def scraper3():
    try:
        r3 = requests.get("http://www.aps.dz")
        unicode_str3 = r3.content.decode('utf8')
        encoded_str3 = unicode_str3.encode("utf-8")
    except:
        print("request failed try again")
        return
    if r3.status_code == 200:

        soup = bf(encoded_str3, "html.parser")
        title = soup.find_all("h3", {"class": "allmode-title"})
        img = soup.find_all('div', {'class': 'allmode-img-top'})
        img = img + soup.find_all('div', {'class': 'allmode-img'})
        array = []
        c = 0
        for i in img:
            im = bf(str(i), "html.parser")
            try:
                im = im.find_all('img')
                im = im[0]["src"]
                array.append(im)
            except:
                array.append("https://i.ibb.co/1z2d99g/aps.jpg")
        for i in title:
            link = bf(str(i), "html.parser")
            link = link.find_all('a')
            link = link[0]['href']
            articles(title=i.get_text().encode("utf-8"),link="http://www.aps.dz"+link,img="http://www.aps.dz"+array[c],category=category(str(i.get_text().encode("utf-8")),0)).save()
            c=c+1

def scraper4():
    #   try to send a get request to the websites
    try:
        url = "https://tsa-algerie.com"
        working_proxy = check_proxies()
        if working_proxy != 0:
            scraper = cfscrape.create_scraper()
            proxies = {"http": working_proxy, "https": working_proxy}
            r4 = scraper.get(url, proxies=proxies, allow_redirects=True, timeout=(10, 30))
            unicode_str4 = r4.content.decode('utf8')
            encoded_str4 = unicode_str4.encode("utf-8")
            if r4.status_code == 200:
                soup = bf(encoded_str4, "html.parser")
                title = soup.find_all('h2', {'class': 'ntdga__title transition'})
                for i in range(0, 10):
                    link = bf(str(title[i].encode("utf-8")), "html.parser")
                    link = link.find_all('a')
                    link = link[0]["href"]
                    articles1.append(str( + ": " + str(link)).replace(",", ""))
                    articles(title=title[i].get_text().encode("utf-8"),link=link,img="https://i.ibb.co/QMZ7VBg/tsa.jpg",category=category(str(i.get_text().encode("utf-8")),0)).save()
                
                
        else:
            print("no working proxy found")
    #   if request failed
    except:
        print("request failed try again")
scraper4()
        # Create your views here.
def index(request):
    articles.objects.all().delete()
    scraper1()
    scraper2()
    scraper3()
    scraper4()
    sport = articles.objects.filter(category="sport")
    health = articles.objects.filter(category="health")
    science = articles.objects.filter(category="science")
    context={"sport":sport,"health":health,"science":science}
   
    return render(request,'gui/index.html', context)