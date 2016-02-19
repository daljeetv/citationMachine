
#!/usr/bin/env python


######################################################
#
# Citation Finder - instant external link search via the command line
# Written by Daljeet Virdi (daljeetv@gmail.com)
#
######################################################


import httplib
import pickle
import argparse
import glob
import os
import random
import re
import requests
import sys
import urlparse
import unicodedata
import httplib2

from . import __version__

from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError
from requests.exceptions import SSLError
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import SoupStrainer

# Handle unicode between Python 2 and 3
# http://stackoverflow.com/a/6633040/305414
if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

if os.getenv('CITATION_MACHINE_DISABLE_SSL'):  # Set http instead of https
    SEARCH_URL = 'http://{0}'
else:
    SEARCH_URL = 'https://{0}'


URL = os.getenv('CITATION_MACHINE_URL') or 'lesswrong.com'

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)
ANSWER_HEADER = u('--- Answer {0} ---\n{1}')
NO_ANSWER_MSG = '< no answer given >'

#write it using format: www.yoursite.com
startWebSite = "http://www.lemonade.io/"
prefixes = ["www.", "http://", "https://"]

def is_absolute(url):
    return bool(urlparse.urlparse(url).path)

# This function gets all the links in the file and stores them in a set.
def clearUrlAndMakeAbsolute(url_path):
    if(url_path == None):
        return False, ""
    else:
        contained = [x for x in prefixes if x in url_path]
        if len(contained) != 0:
            return True, "http://" + url_path.split(contained[0])[1]
        else:
            return True, "http://" + url_path

def addCleanLink(link_temp, url_path):
    link_temp = normalizeUnicode(link_temp)
    if (isWebsite(link_temp)):
        return link_temp
    else:
        return url_path + link_temp


def isWebsite(link_temp):
    return ("www" in link_temp) or("https://" in link_temp) or ("http:" in link_temp)


def normalizeUnicode(link_temp):
    return unicodedata.normalize('NFKD', link_temp).encode('ascii', 'ignore')


def getAllLinks(url_path):
    links = set()
    hdr, status, url_path = createRequest(url_path)
    if(status and startWebSite in url_path):
        http = httplib2.Http()
        try:
            status, response = http.request(url_path, headers=hdr)
        except (httplib2.RedirectLimit, httplib2.ServerNotFoundError, UnicodeError, httplib2.RelativeURIError, httplib.InvalidURL):
            return 'bad'
        print url_path
        # print status
        try:
            for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
                if link.has_key('href'):
                    link_temp = link.get('href')
                    if("#content" not in link_temp):
                        links.add(addCleanLink(link_temp, url_path))
        except (UnicodeEncodeError):
            return 'bad'
    return links


def writeSetToFile(allSet, startWebSite):
    name = create_file_name(startWebSite)
    with open(name+".p", 'wb') as f:
        pickle.dump(allSet, f)


def create_file_name(startWebSite):
    contained = [x for x in prefixes if x in startWebSite]
    if len(contained)!=0:
        return startWebSite.split(contained[0])[1].split(".")[0]
    else:
        return startWebSite


if __name__ == "__main__":
    allLinks = [startWebSite]
    visited = []
    for key in allLinks:
        # mark it as visited.
        if key not in visited:
            visited.append(key)
            # go to all the links in that link
            links = getAllLinks(key)
            # add all links we haven't seen before
            if (links is not None):
                allLinks.extend(links)
                allSet = set(allLinks)
                writeSetToFile(allSet, startWebSite)
    for link in allLinks:
        print link


def get_instructions(args):
    links = get_links(args['query'])
    if not links:
        return False
    answers = []
    append_header = args['num_answers'] > 1
    initial_position = args['pos']
    for answer_number in range(args['num_answers']):
        current_position = answer_number + initial_position
        args['pos'] = current_position
        answer = get_answer(args, links)
        if not answer:
            continue
        if append_header:
            answer = ANSWER_HEADER.format(current_position, answer)
        answer = answer + '\n'
        answers.append(answer)
    return '\n'.join(answers)


def find_links_from_webpage(args):
    args['query'] = ' '.join(args['query']).replace('?', '')
    try:
        return get_instructions(args) or 'Sorry, couldn\'t find any help with that topic\n'
    except (ConnectionError, SSLError):
        return 'Failed to establish network connection\n'

def get_parser():
    parser = argparse.ArgumentParser(description='instant external link search via the command line')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*',
                        help='the question to answer')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if not args['query']:
        parser.print_help()
        return

    if os.getenv('CITATION_LINK_COLORIZE'):
        args['color'] = True

    if sys.version < '3':
        print(find_links_from_webpage(args).encode('utf-8', 'ignore'))
    else:
        print(find_links_from_webpage(args))


if __name__ == '__main__':
    command_line_runner()


