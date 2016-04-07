# How to use:
# python jsonparser.py <old.json> <new.json> <media-url-file>

import requests
import json
import os
import sys

POSTER_STATIC = "http://pressplaytv.in/static/posters/"
STREAM_STATIC = "http://pressplaytv.in/stream/"
DOWNLOAD_STATIC = "http://pressplaytv.in/download/"
UNCHAINED_STATIC = "http://pressplaytv.in/stream/unchained/"

filepath = sys.argv[1]
newfilepath = sys.argv[2]
mp4filepath = sys.argv[3]

dirlist = ['contentitems', 'sponsoritems', 'channelitems']

for dirname in dirlist:
    if not os.path.exists(dirname):
        os.makedirs(dirname)

with open(filepath, 'r') as infile:
    data = infile.read()

readjson = json.loads(data)

feeds = readjson['feeds']
key_list = ['channel', 'content', 'collection']
localurl = {}

channel_list = set()
content_list = set()
sponsor_list = set()

for itemkey in key_list:
    for key, value in readjson[itemkey].iteritems():
        tempdata = value['itemData']

        url = tempdata['posterSmall']
        channel_list.add(url)
        value['itemData']['posterSmall'] = POSTER_STATIC+url.split('/')[-1]

        url = tempdata['poster']
        channel_list.add(url)
        value['itemData']['poster'] = POSTER_STATIC+url.split('/')[-1]

        if tempdata['type'] == 'video':
            url = tempdata['localUrl']
            content_id = tempdata['ppId']
            localurl[content_id] = url
            tempurl = url.split('/')[-1].split('.')
            content_list.add(url)
            value['itemData']['localUrl'] = STREAM_STATIC+str(content_id)+"/"+str(tempurl[1])
            value['itemData']['downloadUrl'] = DOWNLOAD_STATIC+str(content_id)+"/"+str(tempurl[1])

        # print value['itemData']['poster']
        # print value['itemData']['posterSmall']

        if 'preRollPool' in tempdata:
            # print tempdata
            url = tempdata['preRollPool'][0]['playbackUrl']
            sponsor_list.add(url)
            tempurl = url.split('/')[-1].split('.')
            value['itemData']['preRollPool'][0]['playbackUrl'] = UNCHAINED_STATIC+str(tempurl[0])+"/"+str(tempurl[1])
            # print value['itemData']['preRollPool'][0]['playbackUrl']

        if 'topBarSponsor' in tempdata:

            url = tempdata['topBarSponsor']['logo']
            sponsor_list.add(url)
            value['itemData']['topBarSponsor']['logo'] = POSTER_STATIC+url.split('/')[-1]
            # print value['itemData']['topBarSponsor']['logo']

            url = tempdata['topBarSponsor']['image']
            sponsor_list.add(url)
            value['itemData']['topBarSponsor']['image'] = POSTER_STATIC+url.split('/')[-1]

            if value['itemData']['topBarSponsor']['packageName'] != '':
                value['itemData']['topBarSponsor']['downloadUrl'] = 'http://pressplaytv.in/download-app/'+value['itemData']['topBarSponsor']['ppId']+'/ANDROID'

            # print value['itemData']['topBarSponsor']['image']

        try:
            if value['itemContents'] is not None and len(value['itemContents']) > 0:
                for i, content in enumerate(value['itemContents']):
                    for j, faltudata in enumerate(content):
                        if faltudata['type'] in ['channel', 'video', 'collection']:
                            url = faltudata['poster']
                            content_list.add(url)
                            value['itemContents'][i][j]['poster'] = POSTER_STATIC+url.split('/')[-1]

                            url = faltudata['posterSmall']
                            content_list.add(url)
                            value['itemContents'][i][j]['posterSmall'] = POSTER_STATIC+url.split('/')[-1]


                        if faltudata['type'] not in ['channel', 'image_ad']:
                            url = faltudata['localUrl']
                            content_id = faltudata['ppId']
                            content_list.add(url)
                            localurl[content_id] = url
                            tempurl = url.split('/')[-1].split('.')
                            value['itemContents'][i][j]['localUrl'] = STREAM_STATIC+str(content_id)+"/"+str(tempurl[1])
                            value['itemContents'][i][j]['downloadUrl'] = DOWNLOAD_STATIC+str(content_id)+"/"+str(tempurl[1])
                            # print faltudata['localUrl']
                            # print faltudata['downloadUrl']

                        elif faltudata['type'] == 'image_ad':
                            url = faltudata['poster']
                            sponsor_list.add(url)
                            value['itemContents'][i][j]['poster'] = POSTER_STATIC+url.split('/')[-1]
                            value['itemContents'][i][j]['sponsorInfo']['downloadUrl'] = 'http://pressplaytv.in/download-app/'+value['itemContents'][i][j]['sponsorInfo']['ppId']+'/ANDROID'

                            url = faltudata['sponsorInfo']['logo']
                            sponsor_list.add(url)
                            value['itemContents'][i][j]['sponsorInfo']['logo'] = POSTER_STATIC+url.split('/')[-1]

                            url = faltudata['sponsorInfo']['image']
                            sponsor_list.add(url)
                            value['itemContents'][i][j]['sponsorInfo']['image'] = POSTER_STATIC+url.split('/')[-1]

                        elif faltudata['type'] == 'channel':
                            if 'preRollPool' in faltudata:
                                url = faltudata['preRollPool'][0]['playbackUrl']
                                sponsor_list.add(url)
                                tempurl = url.split('/')[-1].split('.')
                                value['itemContents'][i][j]['preRollPool'][0]['playbackUrl'] = UNCHAINED_STATIC+str(tempurl[0])+"/"+str(tempurl[1])

                            if 'topBarSponsor' in faltudata:
                                url = faltudata['topBarSponsor']['logo']
                                sponsor_list.add(url)
                                faltudata['topBarSponsor']['logo'] = POSTER_STATIC+url.split('/')[-1]

                                url = faltudata['topBarSponsor']['image']
                                sponsor_list.add(url)
                                value['itemContents'][i][j]['topBarSponsor']['image'] = POSTER_STATIC+url.split('/')[-1]

                                if faltudata['topBarSponsor']['packageName'] != '':
                                    faltudata['topBarSponsor']['downloadUrl'] = 'http://pressplaytv.in/download-app/'+faltudata['topBarSponsor']['ppId']+'/ANDROID'

        except TypeError, e:
            print e
            continue

for newkey, value in readjson['feeds'].iteritems():
    for i, item in enumerate(value):
        for j, faltudata in enumerate(item):
            if faltudata['type'] in ['channel', 'video', 'collection']:
                url = faltudata['poster']
                channel_list.add(url)
                value[i][j]['poster'] = POSTER_STATIC+url.split('/')[-1]

                url = faltudata['posterSmall']
                channel_list.add(url)
                value[i][j]['posterSmall'] = POSTER_STATIC+url.split('/')[-1]

            if faltudata['type'] != 'image_ad' and faltudata['type'] != 'channel':
                if 'localUrl' in faltudata:
                    url = faltudata['localUrl']
                    content_id = faltudata['ppId']
                    content_list.add(url)
                    localurl[content_id] = url
                    tempurl = url.split('/')[-1].split('.')
                    value[i][j]['localUrl'] = STREAM_STATIC+str(content_id)+"/"+str(tempurl[1])
                    value[i][j]['downloadUrl'] = "http://pressplaytv.in/dowload/"+str(content_id)+"/"+str(tempurl[1])

            elif faltudata['type'] == 'image_ad':
                url = faltudata['poster']
                sponsor_list.add(url)
                value[i][j]['poster'] = POSTER_STATIC+url.split('/')[-1]

                url = faltudata['sponsorInfo']['logo']
                sponsor_list.add(url)
                #####nanda##
                value[i][j]['sponsorInfo']['downloadUrl']='http://pressplaytv.in/download-app/'+faltudata['sponsorInfo']['ppId']+'/ANDROID'
                value[i][j]['sponsorInfo']['logo'] = POSTER_STATIC+url.split('/')[-1]

                url = faltudata['sponsorInfo']['image']
                sponsor_list.add(url)
                value[i][j]['sponsorInfo']['image'] = POSTER_STATIC+url.split('/')[-1]

            elif faltudata['type'] == 'channel':
                if 'preRollPool' in faltudata:
                    url = faltudata['preRollPool'][0]['playbackUrl']
                    sponsor_list.add(url)
                    tempurl = url.split('/')[-1].split('.')
                    value[i][j]['preRollPool'][0]['playbackUrl'] = UNCHAINED_STATIC+str(tempurl[0])+"/"+str(tempurl[1])

                if 'topBarSponsor' in faltudata:
                    url = faltudata['topBarSponsor']['logo']
                    sponsor_list.add(url)
                    value[i][j]['topBarSponsor']['logo'] = POSTER_STATIC+url.split('/')[-1]

                    url = faltudata['topBarSponsor']['image']
                    sponsor_list.add(url)
                    value[i][j]['topBarSponsor']['image'] = POSTER_STATIC+url.split('/')[-1]

                    if faltudata['topBarSponsor']['packageName'] != '':
                        faltudata['topBarSponsor']['downloadUrl'] = 'http://pressplaytv.in/download-app/'+faltudata['topBarSponsor']['ppId']+'/ANDROID'

# for saving new json
with open(newfilepath, 'w') as data_file:
    data_file.write(json.dumps(readjson))
data_file.close()

print 'Converted json:\t', newfilepath

outfile2 = open(mp4filepath, 'w')
for key, value in localurl.iteritems():
    split_name = str(value).split('/')[-1].split('.')
    raw_id = split_name[0]
    extension = split_name[1]
    old_name = "%s.%s" % (raw_id, extension)
    new_name = "%s.%s" % (key, extension)
    outfile2.write('%s,%s,%s\n' % (old_name, new_name, value))

outfile2.close()
print 'Media Url File:\t', mp4filepath
print 'Content Items:\t', len(localurl)
error_file = open('others/errorlinks.txt', 'w')

def download_file(url, directory):
    local_filename = url.split('/')[-1]
    filepath = '%s/%s' % (directory, local_filename)
    if os.path.isfile(filepath):
        print 'File already exists...' + local_filename
    else:
        print 'Downloading... ' + local_filename
        try:
            r = requests.get(url, stream=True, timeout=300)
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            f.close()
        except:
            print 'ERROR: ', url
            error_file.write(url + '\n')
    return True

master_list = list(channel_list) + list(content_list) + list(sponsor_list)

# for downloading files


for item in master_list:
    try:
        if bool(item.count('pp-raw-content')) is False:
            if bool(item.count('com/pp-content')) or bool(item.count('com/pp-raw-content')):
                download_file(item, 'contentitems')
            elif bool(item.count('com/pp-sponsor')):
                download_file(item, 'sponsoritems')
            else:
                download_file(item, 'channelitems')
    except Exception, e:
        print e
        continue
