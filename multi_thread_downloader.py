# -*- coding: utf-8 -*-

import threading
import urllib2
import sys
max_thread = 10
# init thread lock
lock = threading.RLock()
class Downloader(threading.Thread):
    def __init__(self, url, start_size, end_size, fobj, buffer):
        self.url = url
        self.buffer = buffer
        self.start_size = start_size
        self.end_size = end_size
        self.fobj = fobj
        threading.Thread.__init__(self)
    def run(self):
        with lock:
            print 'starting: %s' % self.getName()
        self._download()
    def _download(self):
        """
            download 
        """
        req = urllib2.Request(self.url)
        # add http header range, set the downloading size
        req.headers['Range'] = 'bytes=%s-%s' % (self.start_size, self.end_size)
        f = urllib2.urlopen(req)
        # init the offset of file object for current thread
        offset = self.start_size
        while 1:
            block = f.read(self.buffer)
            # exit if current thread finish downloads
            if not block:
                with lock:
                    print '%s done.' % self.getName()
                break
            # lock thread when writing data
            # use with lock to replace lock.acquire
            # require python >= 2.5
            with lock:
                sys.stdout.write('%s saving block...' % self.getName())
                # set offset of file object
                self.fobj.seek(offset)
                # write blocks
                self.fobj.write(block)
                offset = offset + len(block)
                sys.stdout.write('done.\n')

def main(url, thread=3, save_file='', buffer=1024):
    # max threads can't exceed than max_thread
    thread = thread if thread <= max_thread else max_thread
    # get file size
    req = urllib2.urlopen(url)
    size = int(req.info().getheaders('Content-Length')[0])
    # init file object
    fobj = open(save_file, 'wb')
    # calculate the http range size for each thread
    avg_size, pad_size = divmod(size, thread)   #divmod(x, y) -> (quotient, remainder)
    plist = []
    for i in xrange(thread):
        start_size = i*avg_size
        end_size = start_size + avg_size - 1
        if i == thread - 1:
            # final thread add pad_size
            end_size = end_size + pad_size + 1
        t = Downloader(url, start_size, end_size, fobj, buffer)
        plist.append(t)
    # start thread
    for t in plist:
        t.start()
    # wait for all threads done
    for t in plist:
        t.join()
    # close file object
    fobj.close()
    print 'Download completed!'
if __name__ == '__main__':
    #url = r'http://cdn1.mydown.yesky.com/soft/201405/chromeinstall-7u55.exe'
    #main(url=url, thread=10, save_file='test.exe', buffer=4096)
    pass
    