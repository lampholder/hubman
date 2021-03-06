"""Github.py"""

from hubman.github.issues import Issue
from hubman.github.issues import IssueFetcher
from hubman.github.issues import TimelineFetcher

class Github(object):
    """Aggregates all of the Github interface functionality"""

    def __init__(self, auth):
        self.auth = auth
        self.issue_fetcher = IssueFetcher()
        self.timeline_fetcher = TimelineFetcher(self.auth)

    def issues(self, repos, query):
        for json_issue in self.issue_fetcher.fetch(repos,
                                                   query.to_github_query_string(),
                                                   self.auth):
            issue = Issue.from_json_and_timeline_provider(json_issue, self.timeline_fetcher)
            if query.matches(issue):
                yield issue
