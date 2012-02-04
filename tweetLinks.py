# My app

import tweepy
import sys
import urllib2
import StringIO
import BeautifulSoup
import re
import gzip

import tinyurl
import zlib

from config import Config
from optparse import OptionParser
#tinyurl.create_one('http://google.com/')

#CONSUMER_KEY = 'DgRSSKfbfe5ORNyQ3PJy5g'
#CONSUMER_SECRET = 'Mhq5oqKtw81Bd8WZEVA8Fw5L7ddXiOR3LUgL65w21M'
#ACCESS_KEY = '198543195-6nk9wqcy9ITd0cw22mvcqlXjrXUgmRtO5qQZfhZQ'
#ACCESS_SECRET = 'lmHN8fZsPEkJcEKXOJWminMWftFt54G16zYE2HFL2w4'

# Get title from page
#soup = BeautifulSoup.BeautifulSoup(urllib.urlopen("https://www.google.com"))
#print soup.title.string

#f = open(sys.argv[1], 'r')
#auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#api = tweepy.API(auth)

def authenticate_oauth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

def load_configuration(config_file):
    try:
        cfg = Config(config_file)
        CONSUMER_KEY = cfg.CONSUMER_KEY
        CONSUMER_SECRET = cfg.CONSUMER_SECRET
        ACCESS_KEY = cfg.ACCESS_KEY
        ACCESS_SECRET = cfg.ACCESS_SECRET
    except IOError:
        print "Error reading configuration file."
        print "Make sure the file '%s' is correct." %(config_file)
        sys.exit(-1)

def read_file(filename):
    try:
        f = open(filename, 'r')
        for line in f:
            if not line.strip():
                continue
            else:
                data = None
                try:
                    data = urllib2.urlopen(line) 
                except urllib2.HTTPError:
                    print "Error in the http get of ", line
                    continue
                content = data.read()
                if line.find("egotastic"):
                    try:
                        data = StringIO.StringIO(content)
                        gzipper = gzip.GzipFile(fileobj=data)
                        html = gzipper.read()
                    except zlib.error:
                        print "error"
                    except IOError:
                        html = content
                else:
                    html = content
                soup = BeautifulSoup.BeautifulSoup(html)
                title = soup.title.string
                i = title.find(":")
                turl = tinyurl.create_one(line)
    	    if (len(title) + len(turl)) > 140:
	    	if i > 0:
		    	if (i + len(turl) + 1) > 140:
			    	i = 140 - (len(turl) + 1)
    		else:
	    		i = 140 - (len(turl) + 1)
                message = title[:i] + " " + turl
    	    print message
    	    try:
                api.update_status(message)
            except tweepy.error.TweepError:
                print "Duplicated item, skipping."  
            filename.close
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)


def main():
    parser = OptionParser(usage="usage: %prog [options] filename", version="%prog 1.0")
    parser.add_option("-c", "--config-file", 
                      action="store",
                      dest="config_file",
                      default='oauth.cfg',
                      metavar="FILE",
                      help="Read this configuration file not default, oauth.cfg")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("wrong number of arguments")

#    print options
#    print args
    
    load_configuration(options.config_file)
    authenticate_oauth
    read_file(args[0])


if __name__ == '__main__':
    main()




#for line in f:
#        if not line.strip():
#            continue
#        else:
#	    request = urllib2.Request(line)
#	    request.add_header('Accept-encoding', 'gzip,deflate')
#            response = urllib2.urlopen(request)
#            isGZipped = response.headers.get('content-encoding', '').find('gzip') >= 0

#	    if isGZipped:
#                 data = gzip.GzipFile(fileobj=f).read()
#	    print response
#            soup = BeautifulSoup.BeautifulSoup(data)
#            soup.text
            
            #compresseddata = urllib2.urlopen(line)
            #stringdata = urllib.urlopen(line)
            #compressedstream = StringIO.StringIO(compresseddata) 
            #gzipper = gzip.GzipFile(fileobj=stringdata, mode="r")
            #data = gzipper.read()
            #data = zlib.decompress(stringdata)  #compresseddata)  
	    #print gzipper
#            data = None
#            try:
#              data = urllib2.urlopen(line) 
#            except urllib2.HTTPError:
#              print "Error in the http get of ", line
#              continue
#            content = data.read()
            #try:
            ##    html = gzip.GzipFile(fileobj=StringIO.StringIO(content))
            ##except zlib.error:
            #    print "error"
#            if line.find("egotastic"):
#                try:
#                    data = StringIO.StringIO(content)
#                    gzipper = gzip.GzipFile(fileobj=data)
#                    html = gzipper.read()
#                except zlib.error:
#                    print "error"
#                except IOError:
#                    html = content
#            else:
#                html = content
            #print "Help ", html 
#            soup = BeautifulSoup.BeautifulSoup(html)
#            title = soup.title.string
#            i = title.find(":")
#            turl = tinyurl.create_one(line)
#	    if (len(title) + len(turl)) > 140:
#		if i > 0:
#			if (i + len(turl) + 1) > 140:
#				i = 140 - (len(turl) + 1)
#		else:
#			i = 140 - (len(turl) + 1)
#            message = title[:i] + " " + turl
#	    print message
#	    try:
#              api.update_status(message)
#	    except tweepy.error.TweepError:
#               print "Duplicated item, skipping."
#
#f.close;
#sys.exit(0)


# login to twiter and post message

#auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#api = tweepy.API(auth)
#api.update_status(sys.argv[1])
