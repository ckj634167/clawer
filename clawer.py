# coding=utf-8
'''
fetch company info from specified web page
'''
import os
import urllib,urllib2
from BeautifulSoup import BeautifulSoup
import Queue,thread
from threading import Thread
import multi_thread_downloader

__author__='Jack Liu'
__all__=['Clawer']

HELP_MESSAGE=' Usage: python clawer.py <url>'

class Clawer:
    '''
    Clawer class
    '''
    def __init__(self,url,output='pics'):
        '''
        param url: text string
        '''
        self.url = url if url.startswith('http') else 'http://{0}'.format(url)
        self.conn = urllib.urlopen(self.url)
        self.imglist=[]
        self.output = output
        self.queue = Queue.Queue()
        
    def get_imageslist(self):
        '''get links for images'''
        soup = BeautifulSoup(self.conn.read())
        tags = soup.findAll(name='img')
        assert len(tags)>0, 'None element found'
        for t in tags:
            self.imglist.append(t.get('src'))
        self.imglist=self.parse()
        return self.imglist     
    
    def start(self):
        '''download images'''
        
        if len(self.imglist) <= 0:
            self.get_imageslist()
        assert len(self.imglist)>0, \
            'imglist is empty'
        print "download begin..."
        for imurl in self.imglist:
            self.queue.put(imurl)   #produce
    
    def getUrls(self):
        return self.imglist    
      
    def download(self,save_path=os.getcwd(), min_size=92):
        url = self.queue.get()
        filename = url.split("/")[-1]    #fetch filename
        new_path = os.path.join(save_path + '\\' + self.output)
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        dist = os.path.join(new_path, filename)
        #it is too waste to judge image size by get whole image
        #if len(urllib2.urlopen(im).read()) < min_size:
        #  continue
        #get headers info of image which contains 'conetent-length' key, from this key to get value, then compare size, save cost
        connection = urllib2.build_opener().open(urllib2.Request(url))
        if int(connection.headers.dict['content-length']) > min_size:
            urllib.urlretrieve(url, dist)
        print "Done: ", filename
        print "download end..."
    
    
    def parse(self,urllist=[]):
        '''parse url'''
        for url in self.imglist:
            if url.startswith('http://'):
                urllist.append(url)
        return urllist
    
    def closeConnection(self):
        self.conn.close()

if __name__=='__main__':
    import time
    timeIn= time.clock()  
    url = r'http://www.163.com'
    c = Clawer(url)
    c.start()
    count = 0
    for url in c.getUrls():
        filename = url.split("/")[-1]    #fetch filename
        new_path = os.path.join(os.getcwd() + '\\' + 'pic')
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        dist = os.path.join(new_path, filename)
        if count > 10:
            break
        multi_thread_downloader.main(url, thread=10, save_file=dist, buffer=2048)
        count +=1
    c.closeConnection()
    timeUse = time.clock()-timeIn
    print timeUse