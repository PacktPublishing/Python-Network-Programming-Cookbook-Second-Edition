#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 7
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.
# Supply Flickr API key via local_settings.py

import argparse
import json
import requests

try:
    from local_settings import flickr_apikey
except ImportError:
    pass


def collect_photo_info(api_key, tag, max_count):
    """Collects some interesting info about some photos from Flickr.com for a given tag """
    photo_collection = []
    url =  "http://api.flickr.com/services/rest/?method=flickr.photos.search&tags=%s&format=json&nojsoncallback=1&api_key=%s" %(tag, api_key)
    resp = requests.get(url)
    results = resp.json()
    count  = 0
    for p in results['photos']['photo']:
        if count >= max_count:
            return photo_collection
        print ('Processing photo: "%s"' % p['title'])
        photo = {}
        url = "http://api.flickr.com/services/rest/?method=flickr.photos.getInfo&photo_id=" + p['id'] + "&format=json&nojsoncallback=1&api_key=" + api_key
        info = requests.get(url).json()
        photo["flickrid"] = p['id']
        photo["title"] = info['photo']['title']['_content']
        photo["description"] = info['photo']['description']['_content']
        photo["page_url"] = info['photo']['urls']['url'][0]['_content']
    
        photo["farm"] = info['photo']['farm']
        photo["server"] = info['photo']['server']
        photo["secret"] = info['photo']['secret']
    
        # comments
        numcomments = int(info['photo']['comments']['_content'])
        if numcomments:
            #print "   Now reading comments (%d)..." % numcomments
            url = "http://api.flickr.com/services/rest/?method=flickr.photos.comments.getList&photo_id=" + p['id'] + "&format=json&nojsoncallback=1&api_key=" + api_key
            comments = requests.get(url).json()
            photo["comment"] = []
            for c in comments['comments']['comment']:
                comment = {}
                comment["body"] = c['_content']
                comment["authorid"] = c['author']
                comment["authorname"] = c['authorname']
                photo["comment"].append(comment)
        photo_collection.append(photo)
        count = count + 1
    return photo_collection     


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get photo info from Flickr')
    parser.add_argument('--api-key', action="store", dest="api_key", default=flickr_apikey)
    parser.add_argument('--tag', action="store", dest="tag", default='Python')
    parser.add_argument('--max-count', action="store", dest="max_count", default=3, type=int)
    # parse arguments
    given_args = parser.parse_args()
    api_key, tag, max_count =  given_args.api_key, given_args.tag, given_args.max_count
    photo_info = collect_photo_info(api_key, tag, max_count)
    for photo in photo_info:
        for k,v in photo.iteritems():
            if k == "title":
                print ("Showiing photo info....")  
            elif k == "comment":
                "\tPhoto got %s comments." %len(v)
            else:
                print ("\t%s => %s" %(k,v)) 
    
