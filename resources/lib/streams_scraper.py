import simplejson as json
from urllib import urlencode
from urllib2 import urlopen
import re

API_KEY = 'C55C5A3302BF1CA923A7B41A04E5C0F4'  # please don't steal my key
API_URL = 'http://api.ustream.tv/json/'

STATIC_CHANNELS = [{'title': 'Nasa TV',
                    'thumbnail': 'thumbnail',
                    'url': ('rtmp://cp76072.live.edgefcs.net/live/ '
                            'swfUrl="http://www.nasa.gov/templateimages/'
                            'redesign/flash_player/swf/4.5/player.swf" '
                            'pageUrl="http://www.nasa.gov/multimedia/'
                            'nasatv/media_flash.html" '
                            'Playpath=MED-HQ-Flash@42814 live=true')}, ]


def get_streams(only_live=True):
    path = ('user', 'NASAtelevision', 'listAllChannels')
    json_data = __ustream_request(path)
    channels = []
    for channel in json_data['results']:
        if only_live and channel['status'] != 'live':
            log('skipping channel %s because of status: %s'
                % (channel['title'], channel['status']))
        else:
            channels.append({'title': channel['title'],
                             'id': channel['id'],
                             'description': channel['description'],
                             'thumbnail': channel['imageUrl']['medium']})
            print channel['imageUrl']['medium']
    return channels


def get_stream(id):
    path = ('channel', id, 'getInfo')
    json_data = __ustream_request(path)
    channel_url = json_data['results']['url']
    return __generate_rtmp(id, channel_url)


def __ustream_request(path):
    url = API_URL + '/'.join(path) + '?' + urlencode({'key': API_KEY})
    log('__ustream_request opening url=%s' % url)
    response = urlopen(url).read()
    log('__ustream_request finished with %d bytes result' % len(response))
    return json.loads(response)


def __generate_rtmp(id, page_url):
    amf_url = 'http://cdngw.ustream.tv/Viewer/getStream/1/%s.amf' % id
    r_rtmp = re.compile('(rtmp://.+?)\x00')
    r_sname = re.compile('streamName\W\W\W(.+?)[/]*\x00')
    response = urlopen(amf_url).read()
    rtmp_url = re.search(r_rtmp, response).group(1)
    playpath = re.search(r_sname, response).group(1)
    swf_url = urlopen('http://www.ustream.tv/flash/viewer.swf').geturl()
    return ('%s playpath=%s swfUrl=%s pageUrl=%s swfVfy=1 live=true'
            % (rtmp_url, playpath, swf_url, page_url))


def log(text):
    print 'Nasa streams scraper: %s' % text
