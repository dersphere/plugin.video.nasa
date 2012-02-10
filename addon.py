from xbmcswift import Plugin, xbmc, xbmcplugin, xbmcgui, clean_dict
import resources.lib.scraper as scraper

__addon_name__ = 'Nasa'
__id__ = 'plugin.video.nasa'


class Plugin_mod(Plugin):

    def add_items(self, iterable, view_mode=None, sort_method_ids=[]):
        items = []
        urls = []
        for i, li_info in enumerate(iterable):
            items.append(self._make_listitem(**li_info))
            if self._mode in ['crawl', 'interactive', 'test']:
                print '[%d] %s%s%s (%s)' % (i + 1, '', li_info.get('label'),
                                            '', li_info.get('url'))
                urls.append(li_info.get('url'))
        if self._mode is 'xbmc':
            if view_mode:
                xbmc.executebuiltin('Container.SetViewMode(%s)' % view_mode)
            xbmcplugin.addDirectoryItems(self.handle, items, len(items))
            for id in sort_method_ids:
                xbmcplugin.addSortMethod(self.handle, id)
            xbmcplugin.endOfDirectory(self.handle)
        return urls

plugin = Plugin_mod(__addon_name__, __id__, __file__)


@plugin.route('/', default=True)
def show_root_menu():
    __log('show_root_menu start')
    items = []
    items.append({'label': plugin.get_string(30100),
                  'url': plugin.url_for('show_streams')})
    items.append({'label': plugin.get_string(30101),
                  'url': plugin.url_for('show_topics')})

    __log('show_root_menu end')
    return plugin.add_items(items)


@plugin.route('/streams/')
def show_streams():
    __log('show_streams start')
    NasaScraper = scraper.NasaScraper()
    streams = NasaScraper.get_streams()
    items = [{'label': stream['title'],
              'url': stream['url'],
              'is_folder': False,
              'is_playable': True,
             } for stream in streams]
    __log('show_streams finished')
    return plugin.add_items(items)


@plugin.route('/videos/')
def show_topics():
    __log('show_topics started')
    NasaScraper = scraper.NasaScraper()
    topics = NasaScraper.get_video_topics()
    items = [{'label': topic['name'],
              'url': plugin.url_for('show_videos_by_topic',
                                    topic_id=topic['id']),
             } for topic in topics]
    __log('show_topics finished')
    return plugin.add_items(items)


@plugin.route('/videos/<topic_id>/')
def show_videos_by_topic(topic_id):
    __log('show_videos_by_topic started with topic_id=%s' % topic_id)
    NasaScraper = scraper.NasaScraper()
    videos, video_count = NasaScraper.get_videos(topic_id, start=0, limit=15,
                                                 order_method=None, order=None)
    items = [{'label': video['title'],
              'thumbnail': video['thumbnail'],
              'info': {'originaltitle': video['title'],
                       'duration': video['duration'],
                       'plot': video['description'],
                       'date': video['date'],
                       'size': video['filesize'],
                       'credits': video['author'],
                       'genre': '|'.join(video['genres'])},
              'url': plugin.url_for('play', id=video['id']),
              'is_folder': False,
              'is_playable': True,
             } for video in videos]
    __log('show_videos_by_topic finished')
    return plugin.add_items(items, sort_method_ids=(37, 3, 4, 8))


@plugin.route('/video/<id>/')
def play(id):
    __log('play started with id=%s' % id)
    NasaScraper = scraper.NasaScraper()
    video = NasaScraper.get_video(id)
    __log('play finished with video=%s' % video)
    return plugin.set_resolved_url(video['url'])


@plugin.route('/search_station/')
def search():
    __log('search start')
    search_string = None
    keyboard = xbmc.Keyboard('', plugin.get_string(30201))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        search_string = keyboard.getText()
        __log('search gots a string: "%s"' % search_string)
        language = __get_language()
        stations = NasaScraper.search_stations_by_string(language,
                                                         search_string)
        items = __format_stations(stations)
        __log('search end')
        return plugin.add_items(items)


def __log(text):
    xbmc.log('%s addon: %s' % (__addon_name__, text))

if __name__ == '__main__':
    plugin.run()
