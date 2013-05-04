#!/usr/bin/env python3

import httplib2
import links
import lxml.html.html5parser as html5

http = httplib2.Http(".cache")

def donowt(*a, **b): pass

class crawler:
  def __init__(self, base, link_handler=donowt, page_handler=donowt):
    self.base = base
    self.link_handler = link_handler
    self.page_handler = page_handler
    self.urls = {base}
    self.visited = {}
  
  def crawl(self):
    tocrawl = self.urls
    self.visited = set()
    while not len(tocrawl) == 0:
      toadd = set()
      for url in tocrawl:
        self.visited.add(url)
        resp, content = http.request(url, 'GET')
        if resp['status'] == '404' or 'text/html' not in resp['content-type']:
          continue
        
        self.page_handler(resp, content)
        h = html5.document_fromstring(content, guess_charset=False)
        for link in links.links(h, url=url):
          toadd.add(link.dest)
          self.link_handler(link)
      
      for url in toadd: self.urls.add(url)
      tocrawl = (self.urls ^ self.visited)

def main(argv, input, output):
  crawler(argv[1], link_handler=links.print_link).crawl()

if __name__ == '__main__':
  import sys
  main(sys.argv, input=sys.stdin, output=sys.stdout)
