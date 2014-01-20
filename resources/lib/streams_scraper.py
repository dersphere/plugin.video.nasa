#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2012 Tristan Fischer (sphere@dersphere.de)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from urllib2 import urlopen, Request
import re


RE_CID = re.compile('flashvars: \{"cid":(.+?),')
STATIC_URL = 'http://sjc-uhls-proxy.ustream.tv/watch/playlist.m3u8?cid=%s'
STATIC_STREAMS = [
    {
        'title': 'Nasa TV HD',
        'stream_url': ('http://public.infozen.cshls.lldns.net/infozen/public/'
                       'public/public_1000.m3u8'),
        'stream_id': None,
    }, {
        'title': 'ISS Live Stream',
        'stream_url': None,
        'stream_id': 'ISS_LIVE_STREAM',
    }, {
        'title': 'Educational Channel HD',
        'stream_url': ('http://edu.infozen.cshls.lldns.net/infozen/edu/'
                       'edu/edu_1000.m3u8'),
        'stream_id': None,
    }, {
        'title': 'Media Channel HD',
        'stream_url': ('http://media.infozen.cshls.lldns.net/infozen/media/'
                       'media/media_1000.m3u8'),
        'stream_id': None,
    },
]


def get_streams():
    return STATIC_STREAMS


def get_stream(stream_id):
    if stream_id == 'ISS_LIVE_STREAM':
        request = Request('http://www.ustream.tv/channel/live-iss-stream')
        request.add_header(
            'User-Agent',
            ('Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) '
             'AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 '
             'Mobile/11B554a Safari/9537.53')
        )
        response = urlopen(request).read()
        cid = RE_CID.search(response).groups()[0]
        return STATIC_URL % cid
    else:
        raise NotImplementedError('Unknown stream_id')
