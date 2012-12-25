#-*- encoding: utf-8 -*-

import webapp2
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup
from func import *

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    r = minidom.getDOMImplementation()
    d = r.createDocument(None, 'xml', None)
    #x is the root node
    x = d.createElement('xml')
    s = d.createElement('ToUserName')
    t = d.createCDATASection(ToUserName)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('FromUserName')
    t = d.createCDATASection(FromUserName)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('CreateTime')
    t = d.createTextNode(CreateTime)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('MsgType')
    t = d.createCDATASection('news')
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('Content')
    t = d.createCDATASection('蛋蛋十大')
    logging.info(Content)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('ArticleCount')
    t = d.createTextNode('10')
    s.appendChild(t)
    x.appendChild(s)
    #a is the 'Articles' node
    a = d.createElement('Articles')
    for i in range(0, 10):
        topic = db.GqlQuery('SELECT * FROM TopTenTopic WHERE rank = :1', i).get()
        i = d.createElement('item')
        s = d.createElement('Title')
        t = d.createCDATASection(topic.title)
        s.appendChild(t)
        i.appendChild(s)
        s = d.createElement('PicUrl')
        t = d.createCDATASection(topic.authorPic)
        s.appendChild(t)
        i.appendChild(s)
        s = d.createElement('Url')
        t = d.createCDATASection(topic.url)
        s.appendChild(t)
        i.appendChild(s)
        a.appendChild(i)
    x.appendChild(a)
    s = d.createElement('FuncFlag')
    t = d.createTextNode('0')
    s.appendChild(t)
    x.appendChild(s)
    return x.toxml()

def getAuthorPic(url):
    try:
        res = urlfetch.fetch(url).content
        soup = BeautifulSoup(res)
        soup = soup.find('div', attrs = {'class' : 'avatar'}).find('img')
        url = 'http://www.oiegg.com/' + soup.get('src')
        return url
    except Exception:
        return 'http://www.oiegg.com/images/avatars/noavatar.gif'

class FetchHandler(webapp2.RequestHandler):
    def get(self):
        res = urlfetch.fetch('http://www.oiegg.com/index.php').content
        soup = BeautifulSoup(res)
        soup = soup.find('div', attrs = {'class' : 'mainbox forumlist box on-left'})
        soup = soup.findAll('li')
        for i in range(0, len(soup)):
            j = soup[i].findAll('a')[1]
            title = j.get_text()
            url = 'http://www.oiegg.com/' + j.get('href')
            t = db.GqlQuery('SELECT * FROM TopTenTopic WHERE rank = :1', i).get()
            if t.url == url:
                continue
            t.url = url
            t.title = title
            t.authorPic = getAuthorPic(url)
            t.save()
        logging.info('Top ten updated at %s', time.ctime())

app = webapp2.WSGIApplication([
    ('/topten/fetch', FetchHandler)
], debug = True)