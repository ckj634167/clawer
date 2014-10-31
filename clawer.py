# coding=utf-8
'''
fetch company info from specified web page
'''

import urllib
from BeautifulSoup import BeautifulSoup

__author__='Jack Liu'
__all__=['Clawer']


class Clawer:
    '''
    Clawer class
    '''
    def __init__(self,url):
        '''
        param url: text string
        '''
        self.url = url
        self.conn = urllib.urlopen(url)
        
    def get_imageslist(self):
        ilist=[]
        soup = BeautifulSoup(self.conn.read())
        tags = soup.findAll(name='img')
        assert len(tags)>0, 'None element found'
        for t in tags:
            ilist.append(t.get('src'))
        return ilist     
    
    def closeConnection(self):
        self.conn.close()
if __name__=='__main__':
    c = Clawer('http://www.163.com')
    print c.get_imageslist()
    c.closeConnection()