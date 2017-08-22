"""GitHub.py"""
import re

import requests

class GithubClient(object):
    """Base Github accessor class."""

    _url = 'https://api.github.com'

    @classmethod
    def drain(cls, github_response, headers=None, auth=None):
        """A github response is:
             - some JSON
             - maybe another link to follow to get more of that response"""

        while True:
            response_json = github_response.json()
            for json_entity in response_json:
                yield json_entity

            next_url = re.split('<|>', [link for link in github_response.headers['Link'].split(',')
                                        if link[-10:] == 'rel="next"'][0])[1]

            if next_url is None:
                break

            github_response = requests.get(next_url, headers=headers, auth=auth)
