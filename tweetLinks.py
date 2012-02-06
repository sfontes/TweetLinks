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

<<<<<<< HEAD
def authenticate_oauth(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET):
    try:
        print CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        return api
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
=======
def authenticate_oauth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
>>>>>>> 639f7c0e4b08de3365d49bad3d3bd3f9520d3e11

def load_configuration(config_file):
    try:
        cfg             = Config(config_file)
        CONSUMER_KEY    = cfg.CONSUMER_KEY
        CONSUMER_SECRET = cfg.CONSUMER_SECRET
        ACCESS_KEY      = cfg.ACCESS_KEY
        ACCESS_SECRET   = cfg.ACCESS_SECRET
        return CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET
    except IOError:
        print "Error reading configuration file."
        print "Make sure the file '%s' is correct." %(config_file)
        sys.exit(-1)

def read_file(filename, api):
    try:
        f = open(filename, 'r')
        for line in f:
            if not line.strip():
                continue
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
            title = soup.title.string.lstrip(' \t\n\r').replace('\n',' ')
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
        f.close
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

    CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET = load_configuration(options.config_file)
    print CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET
    api = authenticate_oauth(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
    #print api.getstate()
    read_file(args[0], api)

if __name__ == '__main__':
    main()




#for line in f:
#        if not line.strip():
#            continue
#        else:
#       request = urllib2.Request(line)
#       request.add_header('Accept-encoding', 'gzip,deflate')
#            response = urllib2.urlopen(request)
#            isGZipped = response.headers.get('content-encoding', '').find('gzip') >= 0

#       if isGZipped:
#                 data = gzip.GzipFile(fileobj=f).read()
#       print response
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
#       if (len(title) + len(turl)) > 140:
#       if i > 0:
#           if (i + len(turl) + 1) > 140:
#               i = 140 - (len(turl) + 1)
#       else:
#           i = 140 - (len(turl) + 1)
#            message = title[:i] + " " + turl
#       print message
#       try:
#              api.update_status(message)
#       except tweepy.error.TweepError:
#               print "Duplicated item, skipping."
#
#f.close;
#sys.exit(0)


# login to twiter and post message

#auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#api = tweepy.API(auth)
#api.update_status(sys.argv[1])
