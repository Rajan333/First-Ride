import sys
import json
import requests
from copy import deepcopy

REQ_VERSION = sys.argv[1]
CONTENT_API = "http://ammunition.pressplaytv.in"
APP_API = "http://api.pressplaytv.in/v1"

def create_url(api, endpoint, getparams=[]):
    if endpoint[0] == '/':
        endpoint = endpoint[1:]

    url = '/'.join([api, endpoint]) + '?'

    for a_param in getparams:
        url += str(a_param['key']) + '=' + str(a_param['val']) + '&'

    if url[-1] == '?' or url[-1] == '&':
        url = url[:-1]

    return url

# Get total version data from Ammunition
version_data = requests.get(create_url(api=CONTENT_API, endpoint="version/fetch/" + REQ_VERSION)).json()["data"]
version_id = version_data["id"].split('-')[-1]

feeds = {}
content_data = {}
channel_data = {}
collection_data = {}

version_content = set()
version_collections =set()
version_channels = set()

for a_feed in version_data["version_data"]:
    feed_name = a_feed.split('-')[0]

    feeds[feed_name] = []

    for a_channel in version_data["version_data"]["channel-feed"]:
        for a_content in a_channel["content"]:
            if a_content["type"] == "content":
                version_content.add(a_content["id"])

    for a_row in version_data["version_data"]["home-feed"]:
        for an_item in a_row:
            if an_item["type"] == "content":
                version_content.add(an_item["id"])
            elif an_item["type"] == "collection":
                version_collections.add('pp-collection-' + an_item["id"].split('-')[-1])

    for a_row in version_data["version_data"]["collection-feed"]:
        #for an_item in a_row:
        version_collections.add('pp-collection-' + a_row['collection_id'].split('-')[-1])

    for an_item in version_data["version_data"]["channel-feed"]:
        version_channels.add(an_item["channel_id"])

PAGE_NUM = 1
PAGE_LEN = 1000

def add_content(content_id):
    #print str(create_url(api=APP_API, endpoint="content/" + content_id, getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}]))
    a_content = requests.get(create_url(api=APP_API, endpoint="content/" + content_id, getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}])).json()
    del a_content['data']['pageLen']
    del a_content['data']['pageNum']
    content_data[a_content['data']['itemData']['ppId']] = a_content['data']

    ctr = 0
    items_to_delete = []

    if content_data[a_content['data']['itemData']['ppId']]['itemContents'] is None:
        return

    for a_row in content_data[a_content['data']['itemData']['ppId']]['itemContents']:
        for an_item in a_row:
            #print collection_id, an_item['type'], an_item['ppId']

            if an_item['type'] in ['content', 'video', 'audio'] and an_item['ppId'] not in version_content:
                items_to_delete.append(ctr)
        ctr += 1

    #print '======> ', collection_id, items_to_delete

    for an_index in items_to_delete:
        content_data[a_content['data']['itemData']['ppId']]['itemContents'] = [i for j, i in enumerate(content_data[a_content['data']['itemData']['ppId']]['itemContents']) if j not in items_to_delete]

def add_collection(collection_id):
    a_collection = requests.get(create_url(api=APP_API, endpoint="collection/" + collection_id, getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}])).json()
    del a_collection['data']['pageLen']
    del a_collection['data']['pageNum']
    collection_data[a_collection['data']['itemData']['ppId']] = a_collection['data']

    ctr = 0
    items_to_delete = []

    if collection_data[a_collection['data']['itemData']['ppId']]['itemContents'] is None:
        return

    for a_row in collection_data[a_collection['data']['itemData']['ppId']]['itemContents']:
        for an_item in a_row:
            #print collection_id, an_item['type'], an_item['ppId']
            if an_item['type'] == 'collection' and an_item['ppId'] not in version_collections:
                items_to_delete.append(ctr)
            elif an_item['type'] == 'channel' and an_item['ppId'] not in version_channels:
                items_to_delete.append(ctr)
            elif an_item['type'] in ['content', 'video', 'audio'] and an_item['ppId'] not in version_content:
                items_to_delete.append(ctr)
        ctr += 1

    #print '======> ', collection_id, items_to_delete

    for an_index in items_to_delete:
        collection_data[a_collection['data']['itemData']['ppId']]['itemContents'] = [i for j, i in enumerate(collection_data[a_collection['data']['itemData']['ppId']]['itemContents']) if j not in items_to_delete]

def get_image_ad(some_item):
    data_dict = {}
    data_dict['ppId'] = some_item['ad_id']
    data_dict['name'] = ''
    data_dict['type'] = 'image_ad'
    data_dict['status'] = True
    sponsor_info = requests.get(create_url(api=CONTENT_API, endpoint="sponsor/fetch/" + some_item['sponsor_id'])).json()
    data_dict['poster'] = sponsor_info['data']['image_ad_global'][some_item['ad_id']]
    #for an_ad in sponsor_info['data']['image_ads']:
    #    if some_item['id'] in an_ad:
    #        data_dict['poster'] = an_ad[some_item['id']]
    modSponsorInfo = {}
    modSponsorInfo['ppId'] = sponsor_info['data']['sponsor_id']
    modSponsorInfo['name'] = sponsor_info['data']['name']
    modSponsorInfo['logo'] = sponsor_info['data']['logo']
    modSponsorInfo['image'] = sponsor_info['data']['image']
    modSponsorInfo['description'] = sponsor_info['data']['description']
    modSponsorInfo['type'] = "sponsor"
    modSponsorInfo['status'] = True
    modSponsorInfo['descriptionSmall'] = sponsor_info['data']['description_small']
    modSponsorInfo['tagline'] = sponsor_info['data']['tagline']
    modSponsorInfo['url'] = sponsor_info['data']['url']
    modSponsorInfo['packageName'] = sponsor_info['data']['app_package']
    data_dict['sponsorInfo'] = modSponsorInfo
    return data_dict

def get_sponsor(sponsor_id):
    sponsor_info = requests.get(create_url(api=CONTENT_API, endpoint="sponsor/fetch/" + sponsor_id)).json()
    modSponsorInfo = {}
    modSponsorInfo['ppId'] = sponsor_info['data']['sponsor_id']
    modSponsorInfo['name'] = sponsor_info['data']['name']
    modSponsorInfo['logo'] = sponsor_info['data']['logo']
    modSponsorInfo['image'] = sponsor_info['data']['image']
    modSponsorInfo['description'] = sponsor_info['data']['description']
    modSponsorInfo['type'] = "sponsor"
    modSponsorInfo['status'] = True
    modSponsorInfo['descriptionSmall'] = sponsor_info['data']['description_small']
    modSponsorInfo['tagline'] = sponsor_info['data']['tagline']
    modSponsorInfo['url'] = sponsor_info['data']['url']
    modSponsorInfo['packageName'] = sponsor_info['data']['app_package']
    return modSponsorInfo

def get_pre_roll(some_pre_roll):
    data_dict = {}
    data_dict['ppId'] = some_pre_roll['ad_id']
    data_dict['status'] = True
    data_dict['type'] = "pre_roll"
    data_dict['sponsor_id'] = some_pre_roll['sponsor']
    sponsor_info = requests.get(create_url(api=CONTENT_API, endpoint="sponsor/fetch/" + some_pre_roll['sponsor'])).json()
    data_dict['playbackUrl'] = sponsor_info['data']['preroll_global'][some_pre_roll['ad_id']]
    #for a_pre_roll in sponsor_info['data']['preroll']:
    #    if some_pre_roll['preroll_id'] in a_pre_roll:
    #        data_dict['playbackUrl'] = a_pre_roll[some_pre_roll['preroll_id']]
    return data_dict

def add_channel(channel_id):
    a_channel = requests.get(create_url(api=APP_API, endpoint="channel/" + channel_id, getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}])).json()
    del a_channel['data']['pageLen']
    del a_channel['data']['pageNum']
    channel_data[a_channel['data']['itemData']['ppId']] = a_channel['data']

    if 'preRollPool' in channel_data[a_channel['data']['itemData']['ppId']]['itemData']:
        del channel_data[a_channel['data']['itemData']['ppId']]['itemData']['preRollPool']

    if 'topBarSponsor' in channel_data[a_channel['data']['itemData']['ppId']]['itemData']:
        del channel_data[a_channel['data']['itemData']['ppId']]['itemData']['topBarSponsor']

    ctr = 0
    items_to_delete = []
    channel_data[a_channel['data']['itemData']['ppId']]['itemContents'] = []

    for some_channel in version_data["version_data"]["channel-feed"]:
        if some_channel["channel_id"] == channel_id:

            if 'sellable_entities' in some_channel and 'preroll' in some_channel['sellable_entities']:
                if 'preRollPool' not in channel_data[a_channel['data']['itemData']['ppId']]['itemData']:
                    channel_data[a_channel['data']['itemData']['ppId']]['itemData']['preRollPool'] = []
                for a_pre_roll in some_channel['sellable_entities'] ['preroll']:
                    channel_data[a_channel['data']['itemData']['ppId']]['itemData']['preRollPool'].append(deepcopy(get_pre_roll(a_pre_roll)))

            if 'sellable_entities' in some_channel and 'top-bar-sponsor' in some_channel['sellable_entities']:
                channel_data[a_channel['data']['itemData']['ppId']]['itemData']['topBarSponsor'] = deepcopy(get_sponsor(some_channel['sellable_entities']['top-bar-sponsor']))

            for an_item in some_channel["content"]:
                if an_item["type"] == "content":
                    channel_data[a_channel['data']['itemData']['ppId']]['itemContents'].append([deepcopy(content_data[an_item['id']]['itemData'])])
                elif an_item["type"] == "image_ad":
                    channel_data[a_channel['data']['itemData']['ppId']]['itemContents'].append([deepcopy(get_image_ad(an_item))])

    #if channel_id == 'pp-channel-88':
    #    print '======> ', channel_id, json.dumps(channel_data[a_channel['data']['itemData']['ppId']], indent=4)

for an_item in version_collections:
    add_collection(an_item)

for an_item in version_content:
    add_content(an_item)

for an_item in version_channels:
    add_channel(an_item)


for a_feed in version_data["version_data"]:
    feed_name = a_feed.split('-')[0]

    feeds[feed_name] = []

    if feed_name == "home":
        for a_row in version_data["version_data"][a_feed]:
            this_row = []
            for an_item in a_row:
                if an_item["type"] in ["content", "audio", "video"]:
                    content_info = requests.get(create_url(api=APP_API, endpoint='content/' + an_item['id'], getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}])).json()["data"]["itemData"]
                    this_row.append(deepcopy(content_info))
                elif an_item["type"] == "channel":
                    channel_info = requests.get(create_url(api=APP_API, endpoint='channel/' + an_item['id'], getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}])).json()["data"]["itemData"]
                    this_row.append(deepcopy(channel_info))
                elif an_item["type"] == "collection":
                    collection_info = requests.get(create_url(api=APP_API, endpoint='collection/pp-collection-' + an_item['id'].split('-')[-1], getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}])).json()["data"]["itemData"]
                    this_row.append(deepcopy(collection_info))

            feeds[feed_name].append(deepcopy(this_row))

    elif feed_name == "channel":
        count = 0
        this_row = []
        for an_item in version_data["version_data"][a_feed]:
            count += 1
            channel_info = requests.get(create_url(api=APP_API, endpoint='channel/' + an_item['channel_id'], getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}])).json()["data"]["itemData"]
            this_row.append(deepcopy(channel_info))
            if count % 2 == 0:
                feeds[feed_name].append(deepcopy(this_row))
                this_row = []

    elif feed_name == "collection":
        for a_row in version_data["version_data"][a_feed]:
            this_row = []
            #for an_item in a_row:
            #print str(create_url(api=APP_API, endpoint='collection/pp-collection-' + a_row['collection_id'].split('-')[-1], getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}]))
            collection_info = requests.get(create_url(api=APP_API, endpoint='collection/pp-collection-' + a_row['collection_id'].split('-')[-1], getparams=[{'key': 'pageLen', 'val': PAGE_LEN}, {'key': 'pageNum', 'val': PAGE_NUM}])).json()["data"]["itemData"]
            this_row.append(deepcopy(collection_info))

            feeds[feed_name].append(deepcopy(this_row))

final_dump = {
    "version_id": version_id,
    "feeds": feeds,
    "content": content_data,
    "channel": channel_data,
    "collection": collection_data
}

print json.dumps(final_dump, indent=4)
