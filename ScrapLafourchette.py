# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup, Tag, NavigableString, SoupStrainer
import os
import time
import csv
import requests
import webbrowser
import itertools
import numpy as np
'''Top=open("ListeVille.csv","r")
headers = { 'User-Agent' : 'Mozilla/5.0' }
reader = csv.reader(Top, quotechar='"', delimiter = ';')'''

data=[]
user_agent = {'User-Agent': 'Mozilla/5.0'}

url='https://www.lafourchette.com/restaurant+francais+paris'
crawl_url= urllib2.urlopen(url).read()
bs = BeautifulSoup(crawl_url,"html.parser")

ok=bs.find('div',{"class": "pagination"})
nbPage=ok.find_all('li')[len(ok.find_all('li'))-2].find('a').getText().strip()

for i in range(1,int(nbPage)+1):
    url2=url+"#foodTypeTag=434&filters%5BTAG%5D%5Brestaurant_tag%7C434%7C12%5D=on&page="+str(i)
    print i
    crawl_url2 = urllib2.urlopen(url2).read()

    bs2 = BeautifulSoup(crawl_url2)
    
    ListeRestaurant = bs.find_all('li',{"class": "resultItem"})
    
    for s in ListeRestaurant:
        url3='https://www.lafourchette.com'+str(s.find('a')["href"])+"#reviews"
        crawl_url3 = urllib2.urlopen(url3).read()
        bs3 = BeautifulSoup(crawl_url3)
        RestaurantName=bs3.find("h1",{"class":"restaurantSummary-name"}).getText().strip().encode('utf-8')
        try:
            AverageRating=bs3.find("span",{"class":"rating-ratingValue"}).getText().strip()
            NbRating=bs3.find("div",{"class":"reviewsCount reviewsCount--big"}).getText().strip()
            PrixMoyen=bs3.find("div",{"class":"pull-left restaurantSummary-price"}).getText().strip()
            List_tag=[tag.getText().strip() for tag in bs3.find_all("a",{"class":"restaurantTag"})]
        
        
        except AttributeError:
            AverageRating="NA"
            NbRating="NA"
            
        ok2=bs3.find('ul',{"class": "pagination oneline text_right"})
        try:
            nbPageComm=ok2.find_all('li')[len(ok2.find_all('li'))-1].find('a').getText().strip()
        except IndexError:
            nbPageComm=1      
        for l in range(1,int(nbPageComm)+1):
            print l
            url4=url3+"&page="+str(l)
            crawl_url4 = urllib2.urlopen(url4).read()
            bs4 = BeautifulSoup(crawl_url4)
            CommentPage=bs4.find_all('div',{"class": "reviewItem reviewItem--mainCustomer"})
            for c in CommentPage:
                Userinfo=c.find('div',{"class": "reviewItem-profileInfo"}).getText().strip().encode('utf-8')
                #Userid=c.find('div',{"class": "reviewItem-profileInfo"})
                UserRatings=[h.getText().strip() for h in c.find_all('span',{"class": "reviewItem-scoreText"})]
                try:
                    CommentTS=c.find('li',{"class": "reviewItem-date"}).getText().strip().encode('utf-8')
                except AttributeError:
                    CommentTS="NA"
                UserComment=c.find('div',{"class": "reviewItem-customerComment"}).getText().strip().encode('utf-8')
                try:
                    UserCommentAnswer=c.find('div',{"class": "reviewItem reviewItem--answer"}).find('div',{"class": "reviewItem-wrapper"})
                    Answer=UserCommentAnswer.find('div',{"class": "reviewItem-customerComment"}).getText().strip().encode('utf-8')
                    Answerer=UserCommentAnswer.find('span',{"class": "reviewItem-profileInfo"}).getText().strip().encode('utf-8')
                except AttributeError:
                    UserCommentAnswer="NA"
                    Answer="NA"
                    Answerer="NA"
                CommentData=[RestaurantName,AverageRating,PrixMoyen,List_tag,NbRating,Userinfo,UserRatings,CommentTS,UserComment, Answerer, Answer]
                data.append(CommentData)
    """DATA"""

'''Top.close()'''
fname = open("ListComm.csv","wb")
wr = csv.writer(fname, delimiter=';')
wr.writerows(data)   
fname.close()
