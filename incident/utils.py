from urlparse import parse_qs
from urlparse import urlparse
import unittest
# import re

url_test_1 = 'https://www.youtube.com/watch?v=O2Jrdiyc1ws'
url_test_2 = 'https://youtu.be/O2Jrdiyc1ws'

embed_str = """
      <div class="responsive-embed-16by9-iframe-youtube">
        <div class="embed-responsive embed-responsive-16by9">
          <iframe class="embed-responsive-item" src="//www.youtube.com/embed/VIDEO_URL_HERE?rel=0" allowfullscreen></iframe>
        </div>
      </div>"""

TEST_URLS = [
    ('iwGFalTRHDA', 'http://youtube.com/watch?v=iwGFalTRHDA'),
    ('iwGFalTRHDA', 'http://www.youtube.com/watch?v=iwGFalTRHDA&feature=related'),
    ('iwGFalTRHDA', 'https://youtube.com/iwGFalTRHDA'),
    ('n17B_uFF4cA', 'http://youtu.be/n17B_uFF4cA'),
    ('iwGFalTRHDA', 'youtube.com/iwGFalTRHDA'),
    ('n17B_uFF4cA', 'youtube.com/n17B_uFF4cA'),
    ('r5nB9u4jjy4', 'http://www.youtube.com/embed/watch?feature=player_embedded&v=r5nB9u4jjy4'),
    ('t-ZRX8984sc', 'http://www.youtube.com/watch?v=t-ZRX8984sc'),
    ('t-ZRX8984sc', 'http://youtu.be/t-ZRX8984sc'),
    (None, 'http://www.stackoverflow.com'),
    # ('yes', 'erhaleradfa')
]

YOUTUBE_DOMAINS = [
    'youtu.be',
    'youtube.com',
]


def extract_id(url_string):
    # Make sure all URLs start with a valid scheme
    if not url_string.lower().startswith('http'):
        url_string = 'http://%s' % url_string

    url = urlparse(url_string)

    # Check host against whitelist of domains
    if url.hostname.replace('www.', '') not in YOUTUBE_DOMAINS:
        return None

    # Video ID is usually to be found in 'v' query string
    qs = parse_qs(url.query)
    if 'v' in qs:
        return qs['v'][0]

    # Otherwise fall back to path component
    return url.path.lstrip('/')


def get_youtube_embed_str(url_string):
    vurl = extract_id(url_string)
    if vurl is not None:
        # print embed_str.replace('VIDEO_URL_HERE', vurl)
        return embed_str.replace('VIDEO_URL_HERE', vurl)

    else:
        return None


# get_youtube_embed_str(url_test_1)

# if 1 == 1:
#     print extract_id('https://youtfu.be/w3rqdfadfad')
#     print extract_id(url_test_1)
#     print extract_id(url_test_2)


class TestExtractID(unittest.TestCase):

    def test_extract_id(self):
        for expected_id, url in TEST_URLS:
            result = extract_id(url)
            self.assertEqual(
                expected_id, result, 'Failed to extract ID from '
                'URL %r (got %r, expected %r)' % (url, result, expected_id))


if __name__ == '__main__':
    unittest.main()
