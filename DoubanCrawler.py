# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 20:52:22 2015

@author: liuweizhi
"""
import os,sys
import urllib2  
import cookielib
import re  
from BeautifulSoup import BeautifulSoup

class Movie():
    ''' parse the html and retrive the basic information of movies list '''
    def __init__(self):
        self.url = ''
        self.title = ''
        self.year = -9999
        self.type = ''
        self.country = ''
        self.duration = -9999
        self.abstract = ''
        self.star = -9999
        self.votes = -9999
        self.movies = []
        return 
    
    def parse(self, soup, url):
        tmp = Movie()
        # url
        try:
            tmp.url = url
            print tmp.url
        except:
            print '......missing url'
        
        # title 
        try:
            tmp.title = soup.findAll('span', {'property':'v:itemreviewed'})[0].contents[0]
            print tmp.title
        except:
            print '......missing title'
        
        # year
        try:
            tmp.year = re.findall('\((\d*)\)', soup.findAll('span', {'class':'year'})[0].contents[0])[0]
            print tmp.year
        except:
            print '......missing year'
            
        # type
        try:
            type_list = [foo.contents[0] for foo in soup.findAll('span', {'property':'v:genre'})]
            tmp.type = '/'.join(type_list)
            print tmp.type
        except:
            print '......missing type'
        
        # country
        try:
            tmp.country = re.findall('<span class="pl">制片国家/地区:</span>(\D*)<br />\n<span class="pl">语言:</span>', str(soup))[0].strip()
            print tmp.country
        except:
            print '.....missing country'
        
        # duration
        try:
            tmp.duration = re.findall('(\d*)[\S\s]*', soup.findAll('span', {'property':'v:runtime'})[0].contents[0])[0]
            print tmp.duration
        except:
            print '......missing duration'
        
        # abstract
        try:
            tmp.abstract = ''.join([str(foo).strip() for foo in soup.findAll('span', {'property':'v:summary'})[0].contents if str(foo)!='<br />'])
            print tmp.abstract
        except:
            print '......missing abstract'
            
        # star
        try:
            tmp.star = soup.findAll('strong', {'class':'ll rating_num', 'property':'v:average'})[0].contents[0]
            print tmp.star
        except:
            print '......missing star'
            
        # votes
        try:
            tmp.votes = soup.findAll('span', {'property':'v:votes'})[0].contents[0]
            print tmp.votes
        except:
            print '......missing votes'
            
        self.movies.append(tmp)
            
        return

    def write(self, filename):
        reload(sys) 
        sys.setdefaultencoding('utf-8')
        base_dir = os.getcwd()
        f_out = open(os.path.join(base_dir, 'Output', '%s.txt' % filename), 'w')
        f_out.write('标题\t年份\t类型\t国家\t时长\t评分\t人数\t概括\t链接\n')
        for movie in self.movies:
            f_out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n' % 
                        (movie.title, str(movie.year), movie.type, movie.country, 
                         str(movie.duration), str(movie.star), str(movie.votes), 
                         movie.abstract, movie.url))
        f_out.close()
        reload(sys)
        sys.setdefaultencoding('ascii')
        return
        
class Crawler():
    ''' open the specified url and retrive the specificed content '''
    def __init__(self):
        self.url = ''
        self.pattern = {}
        self.html = ''
        self.soup = ''
        self.content = ''
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        return
        
    def retrive(self):
        try:
            issue = self.opener.open(self.url)
        except:
            print 'open url (%s) failed' % self.url
        self.html = issue.read()
        self.soup = BeautifulSoup(self.html)
        self.content = self.soup.findAll(**self.pattern)
        return
   

doulist_id = raw_input('please enter the id of the doulist\n')
url_id = 0
url_increment = 25
MovieItem = Movie()
while(1):
    print '..processing page %d' % (url_id+1)
    ItemCrawler = Crawler()
    ItemCrawler.url = 'http://www.douban.com/doulist/%s/?start=%d&sort=seq' % (doulist_id, url_id*url_increment) 
    ItemCrawler.pattern = {'name':'div', 'attrs':{'class':'title'}}
    ItemCrawler.retrive()
    movie_id = 1
    if ItemCrawler.content:
        for foo in ItemCrawler.content:
            try:
                print '....processing page %d movie %d' % (url_id+1, movie_id)
                MovieCrawler = Crawler()
                MovieCrawler.url = re.findall('<a href="(\S*)" target="_blank">', str(foo))[0]
                MovieCrawler.pattern = {'name':'div', 'attrs':{'id':'content'}}
                MovieCrawler.retrive()
                MovieItem.parse(MovieCrawler.content[0], MovieCrawler.url)
            except:
                print '......failed'
            movie_id +=1
        url_id += 1
    else:
        #print 'retriving %d movies' % ((url_id-1)*url_increment+movie_id)
        break
    
print '..outputting the movie list'
filename = raw_input('please enter the filename you like\n')
MovieItem.write(filename)

    
    
    