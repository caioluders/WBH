import sqlite3
import os
import sys
import argparse
import glob

from urllib.parse import urlparse


def parse_urls(urls, limit):
    subs = set()
    files = set()
    params = set()
    domains = set()

    for u in urls:
        url = urlparse(u)
        domains.add(url.hostname)

        for d in url.netloc.split(".")[:-2]:
            if len(d) <= limit:
                subs.add(d)

        for f in url.path.split("/"):
            if len(f) <= limit:
                files.add(f)

        for tp in url.query.split("&"):
            if len(tp) <= limit:
                params.add(tp.split("=")[0].split("[")[0])

    return {"subdomains": subs, "files": files, "parameters": params, "domains": domains}


def get_chrome_urls():
    if sys.platform == "win32":
        history_chrome_files = glob.glob(os.path.expanduser(
            "~")+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
    else:
        history_chrome_files = glob.glob(os.path.expanduser(
            "~")+"/.config/*chrom*/*/History")

    turls = []

    for f in history_chrome_files:
        conn = sqlite3.connect(f)
        c = conn.cursor()
        c.execute("select url from urls;")
        for x in c.fetchall():
            turls.append(x[0])

    return turls


def get_firefox_urls():
    if sys.platform == "win32":
        history_firefox_files = glob.glob(os.path.expanduser(
            "~")+"\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*\\places.sqlite")
    elif sys.platform == "darwin" :
        history_firefox_files = glob.glob(os.path.expanduser(
            "~")+"/Library/Application Support/Firefox/Profiles/*/places.sqlite")
    else:
        history_firefox_files = glob.glob(os.path.expanduser(
            "~")+"/.mozilla/firefox/*/places.sqlite")

    turls = []

    for f in history_firefox_files:
        conn = sqlite3.connect(f)
        c = conn.cursor()
        c.execute("select url from moz_places;")
        for x in c.fetchall():
            turls.append(x[0])
    return turls


def main(args):
    urls = set()

    if args.chrome:
        [urls.add(u) for u in get_chrome_urls()]
    elif args.firefox:
        [urls.add(u) for u in get_firefox_urls()]
    else:
        [urls.add(u) for u in get_chrome_urls()]
        [urls.add(u) for u in get_firefox_urls()]

    wordlists = parse_urls(urls, args.limit)

    for key, result_list in wordlists.items():
        print(f"{len(result_list)} {key} found!")
        output = open(os.path.join(args.directory, f"{key}.txt"), "w")
        output.writelines("%s\n" % sub for sub in result_list)
        output.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create subdomains, files, parameters and domains wordlists from browser history")
    parser.add_argument('-d', '--directory',
                        help='Directory to save the wordlists', default="./")
    parser.add_argument(
        '-l', '--limit', help="Limit of characters. Default: 40", type=int, default=40)
    parser.add_argument(
        '-c', '--chrome', help="Use Google Chrome to make the wordlists", action="store_true")
    parser.add_argument(
        '-f', '--firefox', help="Use Firefox to make the wordlists", action="store_true")
    args = parser.parse_args()
    main(args)
