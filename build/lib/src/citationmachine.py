
#!/usr/bin/env python


######################################################
#
# Citation Finder - instant external link search via the command line
# Written by Daljeet Virdi (daljeetv@gmail.com)
#
######################################################


import pickle
import argparse
import os
import random
import re
import sys

from pygments.formatters.terminal import TerminalFormatter
import requests


try:
    from urllib.parse import quote as url_quote
except ImportError:
    from urllib import quote as url_quote

try:
    from urllib import getproxies
except ImportError:
    from urllib.request import getproxies

from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.util import ClassNotFound
from requests.exceptions import ConnectionError
from requests.exceptions import SSLError
from bs4 import BeautifulSoup

__version__ = 0.1

# Handle unicode between Python 2 and 3
# http://stackoverflow.com/a/6633040/305414
if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

SEARCH_URL = 'http://{0}'


URL = os.getenv('CITATION_MACHINE_URL') or 'lesswrong.com'

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)
ANSWER_HEADER = u('--- Answer {0} ---\n{1}')
NO_ANSWER_MSG = '< no answer given >'


def get_proxies():
    proxies = getproxies()
    filtered_proxies = {}
    for key, value in proxies.items():
        if key.startswith('http'):
            if not value.startswith('http'):
                filtered_proxies[key] = 'http://%s' % value
            else:
                filtered_proxies[key] = value
    return filtered_proxies

#
# def getAllLinks(url_path):
#     links = set()
#     hdr, status, url_path = createRequest(url_path)
#     if(status and startWebSite in url_path):
#         http = httplib2.Http()
#         try:
#             status, response = http.request(url_path, headers=hdr)
#         except (httplib2.RedirectLimit, httplib2.ServerNotFoundError, UnicodeError, httplib2.RelativeURIError, httplib.InvalidURL):
#             return 'bad'
#         print url_path
#         # print status
#     return links


def writeSetToFile(allSet, startWebSite):
    name = create_file_name(startWebSite)
    with open(name+".p", 'wb') as f:
        pickle.dump(allSet, f)


def create_file_name(startWebSite):
    # contained = [x for x in prefixes if x in startWebSite]
    # if len(contained)!=0:
    #     return startWebSite.split(contained[0])[1].split(".")[0]
    # else:
    return startWebSite


# if __name__ == "__main__":
#     allLinks = [startWebSite]
#     visited = []
#     for key in allLinks:
#         # mark it as visited.
#         if key not in visited:
#             visited.append(key)
#             # go to all the links in that link
#             links = getAllLinks(key)
#             # add all links we haven't seen before
#             if (links is not None):
#                 allLinks.extend(links)
#                 allSet = set(allLinks)
#                 writeSetToFile(allSet, startWebSite)
#     for link in allLinks:
#         print link

def format_output(code, args):
    if not args['color']:
        return code
    lexer = None

    # try to find a lexer using the StackOverflow tags
    # or the web_site arguments
    for keyword in args['web_site'].split() + args['tags']:
        try:
            lexer = get_lexer_by_name(keyword)
            break
        except ClassNotFound:
            pass

    # no lexer found above, use the guesser
    if not lexer:
        try:
            lexer = guess_lexer(code)
        except ClassNotFound:
            return code

    return highlight(code,
                     lexer,
                     TerminalFormatter(bg='dark'))

def is_question(link):
    return re.search('questions/\d+/', link)

def get_link_at_pos(links, position):
    links = [link for link in links if is_question(link)]
    if not links:
        return False

    if len(links) >= position:
        link = links[position-1]
    else:
        link = links[-1]
    return link


prefixes = ["www."]
def cleanLink(url):
    contained = [x for x in prefixes if x in url]
    for prefix in contained:
        url = url.replace(prefix, "")
    return url



def get_links_from_response(resp):
    encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(resp.content, from_encoding=encoding)
    return soup.find_all('a', href=True)


def get_response(url):
    try:
        cleanUrl = cleanLink(url)
        return requests.get(cleanUrl, headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_proxies())
    except requests.exceptions.SSLError as e:
        print('[ERROR] Encountered an SSL Error. Try using HTTP instead of '
              'HTTPS by setting the environment variable "HOWDOI_DISABLE_SSL".\n')
        raise e


def get_links(web_site):
    response = get_response(SEARCH_URL.format(url_quote(web_site)))
    return get_links_from_response(response)

def get_instructions(args):
    links = get_links(args['web_site'])
    links = [x['href'] for x in links]
    if not links:
        return False
    return '\n'.join(links)


def find_links_from_webpage(args):
    args['web_site'] = ' '.join(args['web_site']).replace('?', '')
    try:
        return get_instructions(args) or 'Sorry, couldn\'t find any help with that topic\n'
    except (ConnectionError, SSLError):
        return 'Failed to establish network connection\n'

def citationmachine(args):
    args['web_site'] = ' '.join(args['web_site']).replace('?', '')
    try:
        return get_instructions(args) or 'Sorry, couldn\'t find that website\n'
    except (ConnectionError, SSLError):
        return 'Failed to establish network connection\n'

def get_parser():
    parser = argparse.ArgumentParser(description='instant external link search via the command line')
    parser.add_argument('web_site', metavar='WEBSITE', type=str, nargs='*',
                        help='the question to answer')
    parser.add_argument('-v', '--version', help='displays the current version of howdoi',
                        action='store_true')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    #for testing purposes:


    if args['version']:
        print(__version__)
        return

    if not args['web_site']:
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



