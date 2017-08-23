"""Github.py"""

from hubman.github.issues import Issue
from hubman.github.issues import IssueFetcher
from hubman.github.issues import TimelineFetcher

from requests.auth import HTTPBasicAuth

class Github(object):
    """Aggregates all of the Github interface functionality"""

    def __init__(self):
        self.auth = HTTPBasicAuth('lampholder', '46aad3839190b0a0521b6ff13e7aea8ce857ecb4')
        self.issue_fetcher = IssueFetcher()
        self.timeline_fetcher = TimelineFetcher(self.auth)

    def issues(self, repos, query):
        for json_issue in self.issue_fetcher.fetch(repos, query, self.auth):
            yield Issue.from_json_and_timeline_provider(json_issue, self.timeline_fetcher)
