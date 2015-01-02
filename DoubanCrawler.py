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
            info = sys.exc_info()
            print info[0], ':', info[1]              
        
        # title 
        try:
            tmp.title = soup.findAll('span', {'property':'v:itemreviewed'})[0].contents[0]
            print tmp.title
        except:
            print '......missing title'
            info = sys.exc_info()
            print info[0], ':', info[1]  
            
        # year
        try:
            tmp.year = re.findall('\((\d*)\)', soup.findAll('span', {'class':'year'})[0].contents[0])[0]
            print tmp.year
        except:
            print '......missing year'
            info = sys.exc_info()
            print info[0], ':', info[1]              
            
        # type
        try:
            type_list = [foo.contents[0] for foo in soup.findAll('span', {'property':'v:genre'})]
            tmp.type = '/'.join(type_list)
            print tmp.type
        except:
            print '......missing type'
            info = sys.exc_info()
            print info[0], ':', info[1]              
        
        # country
        try:
            tmp.country = re.findall('<span class="pl">制片国家/地区:</span>(\D*)<br />\n<span class="pl">语言:</span>', str(soup))[0].strip()
            print tmp.country
        except:
            print '.....missing country'
            info = sys.exc_info()
            print info[0], ':', info[1]              
        
        # duration
        try:
            tmp.duration = re.findall('(\d*)[\S\s]*', soup.findAll('span', {'property':'v:runtime'})[0].contents[0])[0]
            print tmp.duration
        except:
            print '......missing duration'
            info = sys.exc_info()
            print info[0], ':', info[1]              
        
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
            info = sys.exc_info()
            print info[0], ':', info[1]              
            
        # votes
        try:
            tmp.votes = soup.findAll('span', {'property':'v:votes'})[0].contents[0]
            print tmp.votes
        except:
            print '......missing votes'
            info = sys.exc_info()
            print info[0], ':', info[1]              
            
        self.movies.append(tmp)
            
        return

    def write(self):
        filename = raw_input('please enter the filename you like\n')
        reload(sys) 
        sys.setdefaultencoding('utf-8')
        base_dir = os.getcwd()
        f_out = open(os.path.join(base_dir, '%s.txt' % filename), 'w')
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
        
class Books():
    def __init__(self):
        self.url = ''
        self.title = ''
        self.author = ''
        self.publisher = ''
        self.year = ''
        self.pages = -9999
        self.isbn = ''
        self.star = -9999
        self.votes = -9999
        self.abstract = ''
        self.books = []
        return
    
    def parse(self, soup, url):
        tmp = Books()
        # url
        try:
            tmp.url = url
            print tmp.url
        except:
            print '......missing url'
            
        # title
        try:
            tmp.title = soup.findAll('span', {'property':'v:itemreviewed'})[0].contents[0].strip()
            print tmp.title
        except:
            print '......missing title'
            
        # author
        try:
            author_list_html = re.split('\s+/\s+', re.findall('<span class="pl"> 作者</span>:([\S\s]*)<span class="pl">出版社:</span>', str(soup))[0])
            author_list = [re.findall('<a class="" href="/search/\S*">([\S\s]*)</a>', foo)[0].strip() for foo in author_list_html]
            tmp.author = '/'.join(author_list)
            print tmp.author
        except:
            print '......missing author'
            info = sys.exc_info()
            print info[0], ':', info[1]            
            
        # publisher
        try:
            tmp.publisher = re.findall('<span class="pl">出版社:</span>([\S\s]*)<br />\s*<span>\s*<span class="pl"> 译者</span>:', str(soup))[0].strip()
            print tmp.publisher
        except:
            print '......missing publisher'
            info = sys.exc_info()
            print info[0], ':', info[1]              
            
        # year
        try:
            tmp.year = re.findall('<span class="pl">出版年:</span>([\S\s]*)<br />\s*<span class="pl">页数:</span>', str(soup))[0].strip()
            print tmp.year
        except:
            print '......missing year'
            info = sys.exc_info()
            print info[0], ':', info[1]              
            
        # pages
        try:
            tmp.pages = re.findall('<span class="pl">页数:</span>\s*(\d*)<br />\s*<span class="pl">定价:</span>', str(soup))[0]
            print tmp.pages
        except:
            print '......missing page'
            info = sys.exc_info()
            print info[0], ':', info[1]              
            
        # isbn
        try:
            tmp.isbn = re.findall('<span class="pl">ISBN:</span>\s*(\S*)\s*<br />', str(soup))[0].strip()
            print tmp.isbn
        except:
            print '......missing isbn'
            
        # star
        try:
            tmp.star = soup.findAll('strong', {'class':'ll rating_num ', 'property':'v:average'})[0].contents[0].strip()
            print tmp.star
        except:
            print '......missing star'
            info = sys.exc_info()
            print info[0], ':', info[1]              
            
        # votes
        try:
            tmp.votes = soup.findAll('span', {'property':'v:votes'})[0].contents[0]
            print tmp.votes
        except:
            print '......missing votes'
            info = sys.exc_info()
            print info[0], ':', info[1]              
            
        # abstract
        try:
            tmp.abstract = str(''.join(map(str, soup.findAll('div', {'class':'intro'})[0].contents))).replace('<p>','').replace('</p>','').strip()
            print tmp.abstract            
        except:
            print '......missing abstract'
            info = sys.exc_info()
            print info[0], ':', info[1]              
                
        self.books.append(tmp)
        

    def write(self):
        filename = raw_input('please enter the filename you like\n')        
        reload(sys) 
        sys.setdefaultencoding('utf-8')
        base_dir = os.getcwd()
        f_out = open(os.path.join(base_dir, '%s.txt' % filename), 'w')
        f_out.write('标题\t作者\t出版社\t出版年\t页数\tISBN\t评分\t人数\t链接\t摘要\n')
        for book in self.books:
            f_out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n' % 
                        (book.title, book.author, book.publisher, book.year, 
                         str(book.pages), book.isbn, str(book.star), str(book.votes),
                         book.url, book.abstract))
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

class Doulist():
    def __init__(self):
        self.doulist_id = -99999
        self.url_id = 0
        self.url_increment = 25
        self.item_type = ''
        return
    
    def init(self):
        self.doulist_id = raw_input('please enter the id of the doulist\n')
        while not(self.item_type in ['movies', 'books']):
            self.item_type = raw_input('please enter the type of the doulist\n (movies/books)\n')        
        if self.item_type == 'movies':
            self.item = Movie()
        elif self.item_type == 'books':
            self.item = Books()
        return
    
    def retrive(self):
        while(1):
            print '..processing page %d' % (self.url_id+1)
            ItemCrawler = Crawler()
            ItemCrawler.url = 'http://www.douban.com/doulist/%s/?start=%d&sort=seq' % (self.doulist_id, self.url_id*self.url_increment) 
            ItemCrawler.pattern = {'name':'div', 'attrs':{'class':'doulist-item'}}
            ItemCrawler.retrive()
            item_id = 1
            if ItemCrawler.content:
                print '....there are %d items in this page %d' % (len(ItemCrawler.content), self.url_id+1) 
                for foo in ItemCrawler.content:
                    print '....processing page %d %s %d' % (self.url_id+1, self.item_type, item_id)
                    try:
                        SubCrawler = Crawler()
                        SubCrawler.url = re.findall('<a href="(\S*)" target="_blank">', str(foo))[0]
                        SubCrawler.pattern = {'name':'div', 'attrs':{'id':'wrapper'}}
                        SubCrawler.retrive()                        
                        self.item.parse(SubCrawler.content[0], SubCrawler.url)
                    except:
                        print '......failed'
                    item_id += 1
                self.url_id += 1
            else:
                print '..Done'
                break
        return
    

Dou = Doulist()
Dou.init()
Dou.retrive()
            

    
    
    