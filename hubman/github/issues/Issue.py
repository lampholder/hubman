"""Issue.py"""
import dateutil.parser

from hubman.github.issues import Event

class Issue(object):

    def __init__(self, repo, issue_number, title, body, created_at,
                 updated_at, state, timeline, labels, assignees,
                 closed_at=None, json_issue=None):
        self.repo = repo
        self.issue_number = issue_number
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at
        self.closed_at = closed_at
        self.state = state
        self.labels = labels if labels is not None else []
        self.assignees = assignees if assignees is not None else []
        self.timeline = timeline
        self._json = json_issue

    @classmethod
    def from_json_and_timeline_provider(cls, json_issue, timeline_provider):
        """Transform a json representation of an issue into a fully hydrated issue
        object, with the help of a timeline provider to fetch the events timeline."""
        repo = json_issue['repository_url'][29:]
        issue_number = json_issue['number']
        title = json_issue['title']
        body = json_issue['body']
        created_at = dateutil.parser.parse(json_issue['created_at'])
        updated_at = dateutil.parser.parse(json_issue['updated_at'])
        closed_at = (dateutil.parser.parse(json_issue['closed_at'])
                     if json_issue['closed_at'] is not None else None)
        state = json_issue['state']
        labels = [label['name'] for label in json_issue['labels']]
        assignees = [assignee['login'] for assignee in json_issue['assignees']]
        timeline = [Event.from_json(json_event) for json_event in
                    timeline_provider.get_timeline(repo, issue_number, updated_at)]

        return cls(repo, issue_number, title, body, created_at, updated_at,
                   state, timeline, labels, assignees, closed_at, json_issue=json_issue)

    def __str__(self):
        return '%s, %s' % (self.repo, self.issue_number)
