# -*- coding: utf-8 -*-
from urllib2 import urlopen
from urlparse import urljoin
from bs4 import BeautifulSoup
#from xml.etree import ElementTree
import string
import Queue

'''Input: url string; Output:html data string'''
class Downloader:    
    def download(self, url,verbose=False):
        response = urlopen(url)        
        if verbose:
            print 'RESPONSE:', response
            print 'URL     :', response.geturl()
    
            headers = response.info()
            status = response.getcode()
            print 'DATE    :', headers['date']
            print 'STATUS  :', status
            print 'HEADERS :'
            print '---------'
            print headers    
    
        data = response.read()
        if verbose:
            print 'LENGTH  :', len(data)
            print 'DATA    :'
            print '---------'
            print data
    
        return data

"""Store Anchor text and link url for Extra Credit Part 2"""
class Anchor:
    text = ""
    link = ""
    def __init__(self, text, link):
        self.text = text
        self.link = link


'''Store html document properties and methods'''
class Document:
    soup = None
    doc_id = ""
    url = ""
    def __init__(self, html_data, url):
        self.soup = BeautifulSoup(html_data)
        token = url.split("/")
        self.doc_id = token[-1]       #cut the last part of url as doc_id. e.g. "MIMS.html"
        self.url = url                #valid URL e.g."http://courses.ischool.berkeley.edu/i206/f13/a6-sandbox/somepage.html"
        
    def get_title(self):
        return self.soup.head.title.get_text()

    def get_words(self):             #include meta tags in the page header for Extra Credit Part 2
        bag_words = {}
        
        for text in self.soup.stripped_strings:
            for word in text.split():
                word = word.strip(string.punctuation).lower()
                if bag_words.get(word) is None:
                    bag_words[word] = 1
                else:
                    bag_words[word] += 1
        return bag_words    
   
    def get_anchors(self, url):     #include anchor text for Extra Credit Part 2
        #print 'a Tags attribute href'
        anchors = {}
        for tag in self.soup.find_all('a'):
            child_url = tag.get('href')
            child_url = urljoin(url, child_url)
            text = tag.get_text()
            anchor = Anchor(text, child_url)
            if anchor.link not in anchors:
                anchors[anchor.link] = anchor
        return anchors.values()
        
'''Using breadth-first search, manage the traverse sequence''' 
class Scheduler:
    url_dic = {}
    tracking_list = []
    crawl_queue = Queue.Queue()
    count = 0   
    
    def add_url(self, url): 
        self.count += 1
        if url not in self.url_dic:
            self.url_dic[url] = 1
            self.tracking_list.append(url)
            self.crawl_queue.put(url)        
    
    def get_next_url(self):
        if self.crawl_queue.empty():
            return None
        else:
            return self.crawl_queue.get()
                
    def print_pages_found(self):
        print """Using breadth-first search\n"""
        print """The pages found in the following squence:"""
        for i, url in enumerate(self.tracking_list):
            print i, url
        print "Total number of pages crawled: %d" % len(self.tracking_list)
        print "Total number of links found: %d" % self.count
        print "Total number of links followed: %d" % (len(self.tracking_list)-1)

"""Build index and retrieve document"""         
class Index_builder:
    reverted_index = {}
    
    def add_word(self, word, doc_id):
        if word != "":
            if (word in self.reverted_index) and (doc_id not in self.reverted_index[word]):
                self.reverted_index[word].append(doc_id)
            elif word not in self.reverted_index:
                self.reverted_index[word]=[doc_id]
            else:
                return
    def print_reverted_index(self):
        key_list = []
        for key in self.reverted_index.keys():
            key_list.append(key)
        print """Listing of all the entries:"""
        key_list.sort()
        for key in key_list:
            print key 
        print "The number of entries: %d" % len(key_list)
       
    def retrieve_doc(self, word):
        if word in self.reverted_index:
            return self.reverted_index[word]
        else:
            return None
"""Process query string"""
class Query:
    query = ""
    def __init__(self, query):
        self.query = query
    def parse_query(self):
        query_list = []
        columns = self.query.split()
        for word in columns:
            if word != "" and word != string.punctuation:
                word = word.strip(string.punctuation).lower()
                query_list.append(word)
        return query_list

"""Aggregate lists of document ids returned by multi words query, for Extra Credit Part 3"""
class Aggregator:   
    def merge_2lists(self, list1, list2):
        if list1 != None and list2 != None:
            return list(set(list1).intersection(set(list2)))
        else:
            return None
    def get_intersect(self,list_of_lists):
        if len(list_of_lists) != 0:
            intersect = list_of_lists[0]
            for i in range(1, len(list_of_lists)):
                intersect = self.merge_2lists(list_of_lists[i],intersect)
                if intersect == None:
                    break
        return intersect        
        
#class Snippet；                     

"""Render result page with two senario: return one or more results, return zero result"""
class Result_Page:
    def render_result_page(self, doc_list):
        html = """<html><body>"""
        
        if len(doc_list) == 0:
            html += "<p>We don't have result for you. Please try another query.</p>"
        else:
            for doc in doc_list:
                html += "<p><a href='" + doc.url +"'>" + doc.get_title() + "</a></p>"        
        html += """</body></html>"""
        result_file = open('search_result.html', 'w')
        result_file.write(html)
        result_file.close()            
        return 'search_result.html'