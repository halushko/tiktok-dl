import sys
import re
import urllib3
import argparse

from urllib.request import Request, urlopen

DEBUG = True
VERBOSE = False
VERSION = sys.version_info[0]


def download_data(uri):
    ua_chrome = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/76.0.3809.100 Safari/537.36").lower()

    if VERSION == 2:
        req = Request(uri, headers={'User-Agent': ua_chrome})
        r1 = urllib3.HTTPResponse.from_httplib(urlopen(req))
        print("getting url data...")
        r1.data = r1.read()
    else:
        http = urllib3.PoolManager(10, headers={'User-Agent': ua_chrome})
        print("getting url data...")
        r1 = http.urlopen('GET', uri)

    return r1


def video_parse(args, r1):
    print("parsing for video url...")

    P = re.compile("contentUrl\":\"(.*?)\"")

    links = P.findall(r1.data.decode('utf-8'))

    if args.debug:
        for link in links:
            print(link)

    if len(links) == 1:
        print("found good video link...", links[0])
    else:
        print("did not find a video link :(", len(links))

    return links


def mainline():
    parser = argparse.ArgumentParser()
    parser.add_argument("uri", help="uri to load")
    parser.add_argument("-v", "--verbose", help="verbose", action="store_true")
    parser.add_argument("-d", "--debug", help="debug this program", action="store_true")
    parser.add_argument("-o", "--output", help="output filename", default="out.mp4")

    args = parser.parse_args()

    print(args)

    if VERSION == 2:
        pass
    else:
        r1 = download_data(args.uri)

        if args.debug and args.verbose:
            print(r1.data)

        if args.debug:
            print("saving debug output to disk...")
            with open("out.html", "wb") as outf:
                outf.write(r1.data)

        links = video_parse(args, r1)

        r2 = download_data(links[0])

        with open(args.output, "wb") as outf:
            outf.write(r2.data)


if __name__ == "__main__":
    mainline()
