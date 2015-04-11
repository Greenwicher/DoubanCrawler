# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 20:52:22 2015

@author: liuweizhi
"""
import os,sys
import urllib.request
import re  
from bs4 import BeautifulSoup

class Movie():
    ''' parse the html and retrive the basic information of movies list '''
    def __init__(self):
        ''' define the basic property of Movie class'''
        self.url = '-'
        self.title = '-'
        self.year = '-'
        self.type = '-'
        self.country = '-'
        self.duration = '-'
        self.abstract = ''
        self.star = '-'
        self.votes = '-'
        self.movies = []
        return 
    
    def parse(self, soup, url):
        ''' parse the BeautifulSoup Tag to obtain the basic information of Movie '''
        
        # retrieve the information and store them in temporary Movie class tmp
        tmp = Movie()
        # url
        try:
            tmp.url = url
            print(tmp.url)
        except:
            print('......missing url')
            info = sys.exc_info()
            print(info[0], ':', info[1])
        
        # title 
        try:
            tmp.title = soup.findAll('span', {'property':'v:itemreviewed'})[0].contents[0]
            print(tmp.title)
        except:
            print('......missing title')
            info = sys.exc_info()
            print(info[0], ':', info[1])
            
        # year
        try:
            tmp.year = str(re.findall('\((\d*)\)', soup.findAll('span', {'class':'year'})[0].contents[0])[0])
            print(tmp.year)
        except:
            print('......missing year')
            info = sys.exc_info()
            print(info[0], ':', info[1])
            
        # type
        try:
            type_list = [foo.contents[0] for foo in soup.findAll('span', {'property':'v:genre'})]
            tmp.type = '/'.join(type_list)
            print(tmp.type)
        except:
            print('......missing type')
            info = sys.exc_info()
            print(info[0], ':', info[1])
        
        # country
        try:
            tmp.country = re.findall('<span class="pl">制片国家/地区:</span>(\D*)<br />\n<span class="pl">语言:</span>', str(soup))[0].strip()
            print(tmp.country)
        except:
            print('.....missing country')
            info = sys.exc_info()
            print(info[0], ':', info[1])
        
        # duration
        try:
            tmp.duration = str(re.findall('(\d*)[\S\s]*', soup.findAll('span', {'property':'v:runtime'})[0].contents[0])[0])
            print(tmp.duration)
        except:
            print('......missing duration')
            info = sys.exc_info()
            print(info[0], ':', info[1])
        
        # abstract
        try:
            tmp.abstract = ''.join([str(foo).strip() for foo in soup.findAll('span', {'property':'v:summary'})[0].contents if str(foo)!='<br />'])
            print(tmp.abstract)
        except:
            print('......missing abstract')
            
        # star
        try:
            tmp.star = str(soup.findAll('strong', {'class':'ll rating_num', 'property':'v:average'})[0].contents[0])
            print(tmp.star)
        except:
            print('......missing star')
            info = sys.exc_info()
            print(info[0], ':', info[1])              
            
        # votes
        try:
            tmp.votes = str(soup.findAll('span', {'property':'v:votes'})[0].contents[0])
            print(tmp.votes)
        except:
            print('......missing votes')
            info = sys.exc_info()
            print(info[0], ':', info[1])
            
        self.movies.append(tmp)
            
        return

    def write(self):
        ''' write the movies doulist into a tab-aligned txt file'''
        filename = input('please enter the filename you like\n')
        base_dir = os.getcwd()
        f_out = open(os.path.join(base_dir, '%s.txt' % filename), 'w', encoding='utf-8')
        f_out.write('标题\t年份\t类型\t国家\t时长\t评分\t人数\t概括\t链接\n')
        for movie in self.movies:
            f_out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n' % 
                        (movie.title, str(movie.year), movie.type, movie.country, 
                         str(movie.duration), str(movie.star), str(movie.votes), 
                         movie.abstract, movie.url))
        f_out.close()
        return
        
class Book():
    ''' parse the html and retrive the basic information of movies list '''
    def __init__(self):
        ''' define the basic property of Books class'''
        self.url = '-'
        self.title = '-'
        self.author = '-'
        self.publisher = '-'
        self.year = '-'
        self.pages = '-'
        self.isbn = '-'
        self.star = '-'
        self.votes = '-'
        self.abstract = '-'
        self.books = []
        return
    
    def parse(self, soup, url):
        ''' parse the BeautifulSoup Tag to obtain the basic information of Book '''
        
        # retrieve the information and store them in temporary Book class tmp        
        tmp = Book()
        # url
        try:
            tmp.url = url
            print(tmp.url)
        except:
            print('......missing url')
            
        # all span container and theri next_sibling
        span_pl=soup.findAll('span',{'class':'pl'})
        span={}
        for foo in span_pl:
            try:
                span[foo.text.strip().replace(':','')]=foo.next_sibling.strip()
            except:
                continue
            
        # title
        try:
            tmp.title = soup.findAll('span', {'property':'v:itemreviewed'})[0].contents[0].strip()
            print(tmp.title)
        except:
            print('......missing title')
            
        # author
        try:
            author_list_html = re.split('\s+/\s+', re.findall('<span class="pl"> 作者</span>:([\S\s]*)<span class="pl">出版社:</span>', str(soup))[0])
            author_list = [re.findall('<a class="" href="/search/\S*">([\S\s]*)</a>', foo)[0].strip() for foo in author_list_html]
            tmp.author = '/'.join(author_list)
            print(tmp.author)
        except:
            print('......missing author')
            info = sys.exc_info()
            print(info[0], ':', info[1])
            
        # publisher
        try:
#            publisher_tuple = re.findall('<span class="pl">出版社:</span>([\S\s]*)<br />\s*<span class="pl">副标题|<span class="pl">出版社:</span>([\S\s]*)<br />\s*<span class="pl">原作名|<span class="pl">出版社:</span>([\S\s]*)<br />\s*<span>\s*<span class="pl"> 译者|<span class="pl">出版社:</span>([\S\s]*)<br />\s*<span class="pl">出版年', str(soup))[0]
#            tmp.publisher = [foo for foo in publisher_tuple if foo][0].strip()
#            #tmp.publisher = re.findall('<span class="pl">出版社:</span>([\S\s]*)<br />', str(soup))[0].strip()
            tmp.publisher = span['出版社']
            print(tmp.publisher)
        except:
            print('......missing publisher')
            info = sys.exc_info()
            print(info[0], ':', info[1])
            
        # year
        try:
#            year_tuple = re.findall('<span class="pl">出版年:</span>([\S\s]*)<br />\s*<span class="pl">页数:</span>|<span class="pl">出版年:</span>([\S\s]*)<br />\s*<span class="pl">定价:</span>', str(soup))[0]
#            tmp.year = str(re.split('\D+', [foo for foo in year_tuple if foo][0].strip())[0])[0:4]
            tmp.year = span['出版年'].strip()[0:4]
            print(tmp.year)
        except:
            print('......missing year')
            info = sys.exc_info()
            print(info[0], ':', info[1])
            
        # pages
        try:
#            tmp.pages = str(re.findall('<span class="pl">页数:</span>\s*(\d*)[\S\s]*<br />\s*<span class="pl">定价:</span>', str(soup))[0])
            tmp.pages = span['页数'].strip()
            print(tmp.pages)
        except:
            print('......missing page')
            info = sys.exc_info()
            print(info[0], ':', info[1])
            
        # isbn
        try:
#            tmp.isbn = re.findall('<span class="pl">ISBN:</span>\s*(\S*)\s*<br />', str(soup))[0].strip()
            tmp.isbn = span['ISBN'].strip()
            print(tmp.isbn)
        except:
            print('......missing isbn')
            
        # star
        try:
            tmp.star = str(soup.findAll('strong', {'class':'ll rating_num ', 'property':'v:average'})[0].contents[0].strip())
            # deal with the books with no star
            if not tmp.star:
                tmp.star = '-'
            print(tmp.star)
        except:
            print('......missing star')
            info = sys.exc_info()
            print(info[0], ':', info[1])
            
        # votes
        try:
            tmp.votes = str(soup.findAll('span', {'property':'v:votes'})[0].contents[0])
            print(tmp.votes)
        except:
            print('......missing votes')
            info = sys.exc_info()
            print(info[0], ':', info[1])
            
        # abstract
        try:
            tmp.abstract = str(''.join(map(str, soup.findAll('div', {'class':'intro'})[0].contents))).replace('<p>','').replace('</p>','').replace('\n','').replace('\r', '').strip()
            print(tmp.abstract)
        except:
            print('......missing abstract')
            info = sys.exc_info()
            print(info[0], ':', info[1])
                
        self.books.append(tmp)
        return

    def write(self):
        ''' write the books doulist into a tab-aligned txt file'''
        filename = input('please enter the filename you like\n')        
        base_dir = os.getcwd()
        f_out = open(os.path.join(base_dir, '%s.txt' % filename), 'w', encoding='utf-8')
        f_out.write('标题\t作者\t出版社\t出版年\t页数\tISBN\t评分\t人数\t链接\t摘要\n')
        for book in self.books:
            f_out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n' % 
                        (book.title, book.author, book.publisher, str(book.year), 
                         str(book.pages), book.isbn, str(book.star), str(book.votes),
                         book.url, book.abstract))
        f_out.close()
        return        
        
class Crawler():
    ''' open the specified url and retrive the specificed content '''
    def __init__(self):
        self.url = ''
        self.pattern = {}
        self.html = ''
        self.soup = ''
        self.content = ''
        return
        
    def retrive(self):
        ''' retrieve the url for specified item in a given page '''
        try:
            issue = urllib.request.urlopen(self.url)
        except:
            print('open url (%s) failed' % self.url)
        self.html = issue.read()
        self.soup = BeautifulSoup(self.html)
        self.content = self.soup.findAll(**self.pattern)
        return

class Doulist():
    ''' instruct how to crawl the doulist page'''
    def __init__(self):
        ''' define the basic property '''
        self.doulist_id = -99999
        self.url_id = 0
        self.url_increment = 25
        self.item_type = ''
        return
    
    def init(self):
        ''' obtain the type of the doulist and generate the corresponding item parser '''
        self.doulist_id = input('please enter the id of the doulist\n')
        while not(self.item_type in ['movies', 'books']):
            self.item_type = input('please enter the type of the doulist\n (movies/books)\n')        
        if self.item_type == 'movies':
            self.item = Movie()
        elif self.item_type == 'books':
            self.item = Book()
        return
    
    def retrive(self):
        ''' retrieve information from many doulist pages '''
        # repeat until the end of the doulist
        while(1):
            print('..processing page %d' % (self.url_id+1))
            # generate the Crawler for a specificed doulist page and obtain the url of books/movies within that page
            ItemCrawler = Crawler()
            ItemCrawler.url = 'http://www.douban.com/doulist/%s/?start=%d&sort=seq' % (self.doulist_id, self.url_id*self.url_increment) 
            ItemCrawler.pattern = {'name':'div', 'attrs':{'class':'doulist-item'}}
            try:
                ItemCrawler.retrive()
                item_id = 1
                # decide whether the crawler run into the end of the doulist
                if ItemCrawler.content:
                    print('....there are %d items in this page %d' % (len(ItemCrawler.content), self.url_id+1))
                    # crawl each books/movies item withn that doulist page
                    for foo in ItemCrawler.content:
                        print('....processing page %d %s %d' % (self.url_id+1, self.item_type, item_id))
                        try:
                            # generate the crawler for the homepage of the corresponding book/movie
                            SubCrawler = Crawler()
                            SubCrawler.url = re.findall('<a href="(\S*)" target="_blank">', str(foo))[0]
                            SubCrawler.pattern = {'name':'div', 'attrs':{'id':'wrapper'}}
                            SubCrawler.retrive()    
                            
                            # for debugging
                            global g_soup; g_soup = SubCrawler.content[0];
                            
                            # parse the BeautifulSoup Tag of the corresponding book/movie homepage
                            self.item.parse(SubCrawler.content[0], SubCrawler.url)
                        except:
                            print('......failed extract %s homepage' % self.item_type)
                        item_id += 1
                    self.url_id += 1                         
                else:
                    # end of the crawling
                    print('..Done')
                    # output the doulist into txt file
                    self.item.write()
                    break
            except:
                    print('open doulist url failed')
                    info = sys.exc_info()
                    print(info[0], ':', info[1])
        return

class Taglist():
    ''' instruct how to crawl the tag list page'''
    def __init__(self):
        ''' define the basic property '''
        self.tag = ''
        self.url_id = 0
        self.url_increment = 20
        self.item_type = ''
        return
    
    def init(self):
        ''' obtain the type of the tag list and generate the corresponding item parser '''
        self.tag = input('please enter the tag name\n')
        while not(self.item_type in ['movies', 'books']):
            self.item_type = input('please enter the type of the tag list\n (movies/books)\n')        
        if self.item_type == 'movies':
            self.item = Movie()
        elif self.item_type == 'books':
            self.item = Book()
        return
    
    def retrive(self):
        ''' retrieve information from many tag list pages '''
        # repeat until the end of the doulist
        while(1):
            print('..processing page %d' % (self.url_id+1))
            # generate the Crawler for a specificed doulist page and obtain the url of books/movies within that page
            ItemCrawler = Crawler()
            if self.item_type== 'movies':
                ItemCrawler.url = 'http://movie.douban.com/tag/%s?start=%d&type=T' % (urllib.parse.quote(self.tag), self.url_id*self.url_increment) 
                ItemCrawler.pattern = {'name':'table', 'attrs':{'width':'100%'}}            
            else:
                ItemCrawler.url = 'http://book.douban.com/tag/%s?start=%d&type=T' % (urllib.parse.quote(self.tag), self.url_id*self.url_increment) 
                ItemCrawler.pattern = {'name':'li','attrs':{'class':'subject-item'}}                
            try:
                ItemCrawler.retrive()
                item_id = 1
                # decide whether the crawler run into the end of the doulist
                if ItemCrawler.content:
                    print('....there are %d items in this page %d' % (len(ItemCrawler.content), self.url_id+1))
                    # crawl each books/movies item withn that doulist page
                    for foo in ItemCrawler.content:
                        print('....processing page %d %s %d' % (self.url_id+1, self.item_type, item_id))
                        try:
                            # generate the crawler for the homepage of the corresponding book/movie
                            SubCrawler = Crawler()
                            if self.item_type == "movies":                                
                                SubCrawler.url = re.findall('<a class="nbg" href="(\S*)" title="\S*">', str(foo))[0]
                            else:
                                SubCrawler.url = re.findall('<a href="(\S*)" onclick=', str(foo))[0]
                            SubCrawler.pattern = {'name':'div', 'attrs':{'id':'wrapper'}}
                            SubCrawler.retrive()    
                            
                            # for debugging
                            global g_soup; g_soup = SubCrawler.content[0];
                            
                            # parse the BeautifulSoup Tag of the corresponding book/movie homepage
                            self.item.parse(SubCrawler.content[0], SubCrawler.url)
                        except:
                            print('......failed extract %s homepage' % self.item_type)
                        item_id += 1
                    self.url_id += 1                         
                else:
                    # end of the crawling
                    print('..Done')
                    # output the doulist into txt file
                    self.item.write()
                    break
            except:
                    print('open tag list url failed')
                    info = sys.exc_info()
                    print(info[0], ':', info[1])
        return

    
def debugger():
    ''' for debugging, return the soup content of the specificed homepage of book/movie'''
    url = input('please enter the url of the homepage\n')
    SubCrawler = Crawler()
    SubCrawler.url = url
    SubCrawler.pattern = {'name':'div', 'attrs':{'id':'wrapper'}}
    SubCrawler.retrive()
    soup = SubCrawler.content[0]
    debug_type=input("Please the type of the object for debugging\n (books/moives)\n")
    if debug_type=="books":
        debug_obj = Book()
    else:
        debug_obj = Movie()
    debug_obj.parse(soup,url)
    return soup

def main():
    # check the user want to retrive information from doulist or tag list
    dou_tag = input('Please enter the resource you want to retrive\n (doulist/tag)\n')
    while(not(dou_tag in ['doulist','tag','d'])):
        dou_tag = input('Invalid Input. Please enter the resource you want to retrive\n (doulist/tag)\n')
    if dou_tag == 'doulist':
        global Dou
        Dou = Doulist()
        Dou.init()
        Dou.retrive()
    elif dou_tag == 'tag':
        global Tag
        Tag = Taglist()
        Tag.init()
        Tag.retrive()
    elif dou_tag == 'd':
        global soup
        soup=debugger()

if __name__ == "__main__":
    main()