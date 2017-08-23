"""TimelineFetcher.py"""
import json

import requests

from hubman.github import GithubClient
from hubman.github.storage import Database
from hubman.github.storage import Timelines

class TimelineFetcher(GithubClient):
    """Responsible for pulling JSON event timelines of an issue back from Github, and
    for doing so via a cache. It's somebody else's job to dress that JSON up nicely."""

    def __init__(self, auth):
        self._cache = TimelineCache()
        self._auth = auth

    def get_timeline(self, repo, issue_number, freshness):
        """Check the cache for a fresh copy of the timeline. If it's not there, grab
        one from the Internet. Returns a list."""
        cached_timeline = self._cache.get_timeline(repo, issue_number, freshness)
        if cached_timeline is None:
            timeline = self._get_timeline_from_internet(repo, issue_number, self._auth)
            self._cache.write_timeline(repo, issue_number, freshness,
                                       json.dumps(timeline))
            return timeline
        else:
            return cached_timeline

    @classmethod
    def _get_timeline_from_internet(cls, repo, issue_number, auth):
        """Returns a generator pulling timeline events from the Internet"""
        headers = {'Accept': 'application/vnd.github.mockingbird-preview'}

        timeline_url = cls._url + '/repos/%s/issues/%d/timeline' % (repo, issue_number)

        github_response = requests.get(timeline_url, headers=headers, auth=auth)

        return list(cls.drain(github_response, headers=headers, auth=auth))

class TimelineCache(object):
    """Responsible for storing cached versions of the timeline data. Not a writethrough
    cache, unfortunately."""

    def __init__(self):
        self.timelines = Timelines()

    def get_timeline(self, repo, issue_number, freshness):
        """Returns the full text of the json dump of the timeline if it's in the cache,
        or None if the cache misses."""
        with Database.connection() as connection:
            timeline = self.timelines.fetch(repo, issue_number, freshness, connection)
            if timeline is None:
                return None
            return json.loads(timeline['timeline'])

    def write_timeline(self, repo, issue_number, freshness, timeline):
        """Writes a timeline to the cache."""
        with Database.connection() as connection:
            self.timelines.create(repo, issue_number, freshness, timeline, connection)
