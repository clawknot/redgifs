#!/usr/bin/env python

"""
The MIT License (MIT)
Copyright (c) 2021-present boobfuck

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import re
import sys
import time
import argparse
import textwrap
from urllib.parse import urlparse, urlencode
from urllib.request import Request, urlopen

__version__ = '1.2.0'

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Download videos from redgifs.com\nVersion: {}'.format(__version__))
parser.add_argument(
    'url',
    default=None,
    nargs='?',
    help='The gif URL. If you want to use [--file] flag then this is can be omitted.')
parser.add_argument(
    '-f', '--file',
    metavar='',
    help='File path of the URLs to download. A file need to be passed when using this flag.')
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-q', '--quite',
    action='store_true',
    help='No verbose outputs.')
group.add_argument(
    '-w', '--wait',
    type=int,
    default=6.9,
    metavar='',
    help='Wait for some seconds between each request (while using -f). Default: 6.9')
group.add_argument(
    '-ns', '--no-save',
    action='store_true',
    help='Don\'t save the video, just return the MP4 URL.')
args = parser.parse_args()

# for verbose printing
vprint = print if not args.quite else lambda *a, **k: None

def check_url(url):
    o = urlparse(url)
    if o.scheme not in ['http', 'https']:
        return TypeError('URL must be of scheme HTTP or HTTPS')

    if 'redgifs' not in o.netloc:
        return TypeError('Invalid URL: %s', o.geturl())

    return o.geturl()

def get_content(url, no_save):
    """Steps in-order.

    * check url
    * request html
    * get content
    """
    url = check_url(url)
    headers = {'User-Agent': 'Mozilla/5.0'}
    request_url = Request(url, headers=headers)
    CONTENT_RE = re.compile(r'https:\/\/[a-z0-9]+.redgifs.com\/\w+.mp4')

    vprint('\n[v] Sending request to', url)
    with urlopen(request_url) as response:

        vprint('[v] Reading and Decoding HTML')
        html = response.read().decode('utf-8')

    content = re.search(CONTENT_RE, html).group(0)
    vprint('[v] Got video data')

    if no_save:
        return content
    
    req = Request(content, headers=headers)
    filename = content.split('/')[::-1][0]
    with urlopen(req) as downloaded:
        vprint('[v] Downloading file..')
        with open(filename, 'wb') as f:
            f.write(downloaded.read())
            vprint('[*] Downloaded:', filename)

def get_from_file(file, wait, no_save):
    """Steps in-order

    * opens file
    * get urls from file
    * get_content from urls
    """
    with open(file) as f:
        urls = [line.strip('\n') for line in f]

    contents = []
    for url in urls:
        content = get_content(url, no_save)
        contents.append(content)
        time.sleep(wait)

    return contents

if __name__ == '__main__':
    try:
        if args.url is not None:
            mp4 = get_content(args.url, args.no_save)
            if args.no_save:
                print(mp4)

        if args.url is None:
            if args.file:
                mp4s = get_from_file(args.file, args.wait, args.no_save)

                if args.no_save:
                    print('\n' + '\n'.join([mp4 for mp4 in mp4s]))
                else:
                    print('\nDownload complete.')
            else:
                parser.print_help(sys.stderr)
                exit(1)

    except KeyboardInterrupt:
        print('\n[!] Keyboard Interrupt\n')
