"""GitHub.py"""
import re

import requests

def _extractNextLinkFromHeader(link_header):
    if link_header is None:
        return None

    next_links = [link for link in link_header.split(',')
                  if link[-10:] == 'rel="next"']

    if len(next_links) == 1:
        return re.split('<|>', next_links[0])[1]

    return None

class GithubClient(object):
    """Base Github accessor class."""

    _url = 'https://api.github.com'

    @classmethod
    def drain(cls, github_response, headers=None, auth=None, fetcher=None):
        """A github response is:
             - some JSON
             - maybe another link to follow to get more of that response"""

        def default_fetcher(response_json):
            """Default fetching strategy - just yield everything in the
            array one by one."""
            for json_entity in response_json:
                yield json_entity

        if fetcher is None:
            fetcher = default_fetcher

        while True:
            response_json = github_response.json()
            for json_entity in fetcher(response_json):
                yield json_entity

            next_url = _extractNextLinkFromHeader(github_response.headers.get('Link',
                                                                              None))

            if next_url is None:
                break

            github_response = requests.get(next_url, headers=headers, auth=auth)
