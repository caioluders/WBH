import sqlite3, os, argparse, glob, itertools
from urllib.parse import urlparse


def parse_urls(urls,limit) :
	subs = set()
	files = set()
	params = set() 

	for u in urls :
		url = urlparse(u)
		for d in url.netloc.split(".")[:-2] :
			if len(d) <= limit : subs.add(d)

		for f in url.path.split("/") :
			if len(f) <= limit : files.add(f)

		for tp in url.query.split("&") :
			if len(tp) <= limit : params.add(tp.split("=")[0].split("[")[0])

	return {"subs":subs,"files":files,"params":params}

def get_chrome_urls() :
	history_chrome_files = glob.glob(os.path.expanduser("~")+"/.config/*chrom*/Default/History")
	
	turls = []

	for f in history_chrome_files :
		conn = sqlite3.connect(f)
		c = conn.cursor()
		c.execute("select url from urls;")
		for x in c.fetchall() :
			turls.append(x[0])
	
	return turls

def get_firefox_urls() :
	history_firefox_files = glob.glob(os.path.expanduser("~")+"/.mozilla/firefox/*/places.sqlite")
	turls = []

	for f in history_firefox_files :
		conn = sqlite3.connect(f)
		c = conn.cursor()
		c.execute("select url from moz_places;")
		for x in c.fetchall() :
			turls.append(x[0])
	
	return turls

def main(args):

	urls = set()
	
	if args.chrome : 
		[ urls.add(u) for u in get_chrome_urls() ]
	elif args.firefox :
		[ urls.add(u) for u in get_firefox_urls() ]
	else :
		[ urls.add(u) for u in get_chrome_urls() ]
		[ urls.add(u) for u in get_firefox_urls() ]

	wordlists = parse_urls(urls,args.limit)

	print("%s subdomains found!" % len(wordlists["subs"]))
	print("%s paths found!" % len(wordlists["files"]))
	print("%s params found!" % len(wordlists["params"]))

	subs = open(os.path.join(args.directory,"subdomains.txt"),"w")
	subs.writelines("%s\n" % sub for sub in wordlists["subs"])	
	subs.close()

	files = open(os.path.join(args.directory,"paths.txt"),"w")
	files.writelines("%s\n" % f for f in wordlists["files"])
	files.close()

	params = open(os.path.join(args.directory,"params.txt"),"w")
	params.writelines("%s\n" % f for f in wordlists["params"])
	params.close()

if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description="Create subdomains and files wordlists from browser history")
	parser.add_argument('-d','--directory', help='Directory to save the wordlists',default="./")
	parser.add_argument('-l','--limit', help="Limit of characters. Default: 40", type=int, default=40)
	parser.add_argument('-c','--chrome',help="Use Google Chrome to make the wordlists",action="store_true")
	parser.add_argument('-f','--firefox',help="Use Firefox to make the wordlists",action="store_true")
	args = parser.parse_args()
	main(args)
