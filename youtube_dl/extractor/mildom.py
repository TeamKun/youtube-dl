# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class MildomIE(InfoExtractor):
    IE_NAME = 'mildom'
    IE_DESC = 'ミルダム'

    _TESTS = [{
        'url': 'https://www.mildom.com/playback/10105254/10105254-c07c5ilaks9dfbt91t60',
        'md5': 'd1a75c0823e2f629128c43e1212760f9',
        'info_dict': {
            'id': 'sm22312215',
            'ext': 'mp4',
            'title': 'Big Buck Bunny',
            'thumbnail': r're:https?://.*',
            'uploader': 'takuya0301',
            'uploader_id': '2698420',
            'upload_date': '20131123',
            'timestamp': int,  # timestamp is unstable
            'description': '(c) copyright 2008, Blender Foundation / www.bigbuckbunny.org',
            'duration': 33,
            'view_count': int,
            'comment_count': int,
        },
        'skip': 'Requires an account',
    }, {
        'url': 'https://m.mildom.com/playback/10105254/10105254-c07c5ilaks9dfbt91t60',
        'only_matching': True,
    }]

    _VALID_URL = r'https?://(?:www\.|m\.)?mildom\.com/(?P<id>[0-9]+)'
    _NETRC_MACHINE = 'mildom'

    def _real_extract(self, url):
        video_id = self._match_id(url)

        # Get video webpage. We are not actually interested in it for normal
        # cases, but need the cookies in order to be able to download the
        # info webpage
        webpage_url = 'http://www.mildom.com/' + video_id
        webpage, handle = self._download_webpage_handle(webpage_url, video_id)

        response = self._download_json(
            'https://cloudac.mildom.com/nonolive/gappserv/live/enterstudio?__platform=web&user_id=%s' % video_id, video_id,
            query={'_format': 'json'},
            headers={'Content-Type': 'application/json'},
            note='Downloading JSON metadata for %s' % video_id)

        manifest = self._extract_f4m_formats(

        )

        meta = response['body']

        return {
            'id': video_id,
            'title': meta['anchor_intro'],
            'formats': meta['ext'],
            'thumbnail': meta['pic'],
            'description': meta['live_intro'],
            'uploader': meta['loginname'],
            'timestamp': meta['live_start_ms'],
            'uploader_id': meta['user_id'],
            'view_count': meta['viewers'],
            'duration': meta['live_start_ms'] - response['ts_ms'],
            'webpage_url': webpage_url,
        }


class MildomPlaybackIE(InfoExtractor):
    IE_NAME = 'mildom'
    IE_DESC = 'ミルダム'

    _TESTS = [{
        'url': 'https://www.mildom.com/playback/10105254/10105254-c07c5ilaks9dfbt91t60',
        'md5': 'd1a75c0823e2f629128c43e1212760f9',
        'info_dict': {
            'id': 'sm22312215',
            'ext': 'mp4',
            'title': 'Big Buck Bunny',
            'thumbnail': r're:https?://.*',
            'uploader': 'takuya0301',
            'uploader_id': '2698420',
            'upload_date': '20131123',
            'timestamp': int,  # timestamp is unstable
            'description': '(c) copyright 2008, Blender Foundation / www.bigbuckbunny.org',
            'duration': 33,
            'view_count': int,
            'comment_count': int,
        },
        'skip': 'Requires an account',
    }, {
        'url': 'https://m.mildom.com/playback/10105254/10105254-c07c5ilaks9dfbt91t60',
        'only_matching': True,
    }]

    _VALID_URL = r'https?://(?:www\.|m\.)?mildom\.com/playback/(?P<user>[0-9]+)/(?P<id>[0-9]+-[0-9a-z]+)'
    _NETRC_MACHINE = 'mildom'

    def _real_extract(self, url):
        video_id = self._match_id(url)

        # Get video webpage. We are not actually interested in it for normal
        # cases, but need the cookies in order to be able to download the
        # info webpage
        webpage_url = 'http://www.mildom.com/playback/' + video_id
        webpage, handle = self._download_webpage_handle(webpage_url, video_id)

        response = self._download_json(
            'https://cloudac.mildom.com/nonolive/videocontent/playback/getPlaybackDetail?v_id=%s' % video_id, video_id,
            query={'_format': 'json'},
            headers={'Content-Type': 'application/json'},
            note='Downloading JSON metadata for %s' % video_id)

        meta = response['body']['playback']

        return {
            'id': video_id,
            'title': meta['title'],
            'formats': meta['video_link'],
            'thumbnail': meta['upload_pic'],
            'description': meta['video_intro'],
            'uploader': meta['author_info']['login_name'],
            'timestamp': meta['publish_time'],
            'uploader_id': meta['user_id'],
            'view_count': meta['view_num'],
            'duration': meta['video_length'],
            'webpage_url': webpage_url,
        }
