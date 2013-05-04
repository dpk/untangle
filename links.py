#!/usr/bin/env python3

import lxml.html.html5parser as html5
from lxml.etree import XPath
from urllib.parse import urljoin

basehref = XPath('/h:html/h:head/h:base[@href]',
             namespaces={'h': 'http://www.w3.org/1999/xhtml'})
linktags = XPath('//h:a[@href] | //h:link[@href] | //h:img[@src] | //h:script[@src]',
             namespaces={'h': 'http://www.w3.org/1999/xhtml'})

def links(h, url='', base=None):
  if base is None: base = url
  basetags = basehref(h)
  if basetags:
    for basetag in basetags:
      base = urljoin(base, basetag.attrib['href'])
  
  def make_link(elt):
    def strip_namespace(tagname): return tagname[tagname.rindex('}')+1:]
    
    tag = strip_namespace(elt.tag)
    rel = elt.attrib['rel'] if 'rel' in elt.attrib else ''
    source = url
    
    attr = 'src' if tag in {'img', 'script'} else 'href'
    dest = urljoin(base, elt.attrib[attr])
    return link(source=source, dest=dest, tag=tag, rel=rel)
  
  return (make_link(elt) for elt in linktags(h))

def main(argv, input, output):
  h = html5.parse(input)
  for link in links(h, url=argv[1]):
    print(link.source, link.dest, link.tag, link.rel, sep="\t", end="\n")

class link:
  def __init__(self, source, dest, tag, rel):
    self.source = source
    self.dest = dest
    self.tag = tag
    self.rel = rel

if __name__ == '__main__':
  import sys
  main(sys.argv, input=sys.stdin, output=sys.stdout)
