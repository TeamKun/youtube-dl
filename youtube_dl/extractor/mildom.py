# coding: utf-8
from __future__ import unicode_literals

import datetime
import functools
import json
import math

from .common import InfoExtractor
from ..compat import (
    compat_parse_qs,
    compat_urllib_parse_urlparse,
)
from ..utils import (
    determine_ext,
    dict_get,
    ExtractorError,
    float_or_none,
    InAdvancePagedList,
    int_or_none,
    parse_duration,
    parse_iso8601,
    remove_start,
    try_get,
    unified_timestamp,
    urlencode_postdata,
    xpath_text,
)


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

    _VALID_URL = r'https?://(?:www\.|m\.)?mildom\.com/playback/(?P<user>[0-9]+)/(?P<id>[0-9]+-[0-9a-z]+)'
    _NETRC_MACHINE = 'mildom'

    def _real_extract(self, url):
        video_id = self._match_id(url)

        # Get video webpage. We are not actually interested in it for normal
        # cases, but need the cookies in order to be able to download the
        # info webpage
        webpage, handle = self._download_webpage_handle(
            'http://www.mildom.com/playback/' + video_id, video_id)
        session_response = self._download_json(
            'https://cloudac.mildom.com/nonolive/videocontent/playback/getPlaybackDetail?v_id=%s' % video_id, video_id,
            query={'_format': 'json'},
            headers={'Content-Type': 'application/json'},
            note='Downloading JSON metadata for %s' % format_id)

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'thumbnail': thumbnail,
            'description': description,
            'uploader': uploader,
            'timestamp': timestamp,
            'uploader_id': uploader_id,
            'view_count': view_count,
            'comment_count': comment_count,
            'duration': duration,
            'webpage_url': webpage_url,
        }
