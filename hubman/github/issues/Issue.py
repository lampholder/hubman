"""Issue.py"""
import dateutil.parser

from hubman.github.issues import Event
from hubman.github.issues import Entity
from hubman.github.issues import Polarity


class Issue(object):

    def __init__(self, repo, number, title, body, created_at,
                 updated_at, state, timeline, labels, assignees,
                 closed_at=None, json_issue=None):
        self.repo = repo
        self.number = number
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

    def rollback(self):
        """Generate a copy of this issue with the most recent event unapplied."""
        event = self.timeline[-1] # Event to roll back
        remaining_events = self.timeline[:-1]

        # These are the only entities we support rolling back so far.
        labels = self.labels
        assignees = self.assignees

        entity_map = {Entity.ASSIGNEE: assignees,
                      Entity.LABEL: labels}

        state = self.state

        ffs_map = {'feature': 'enhancement',
                   'enhancement': 'feature'}

        #XXX: Open/closed state has really messed with this code :(
        if event.entity is not Entity.IGNORED:
            if event.polarity is Polarity.ADDED:
                if event.entity is Entity.OPEN:
                    state = 'closed'
                else:
                    # FFS: Github stores label strings in the event timeline, not ids.
                    if event.payload not in entity_map[event.entity]:
                        event.payload = ffs_map[event.payload]
                    entity_map[event.entity].remove(event.payload)
            elif event.polarity is Polarity.REMOVED:
                if event.entity is Entity.OPEN:
                    state = 'open'
                else:
                    entity_map[event.entity].append(event.payload)

        return Issue(self.repo, self.number, self.title, self.body,
                     self.created_at, self.updated_at, state, remaining_events,
                     labels, assignees, self.closed_at, self._json)

    @classmethod
    def from_json_and_timeline_provider(cls, json_issue, timeline_provider):
        """Transform a json representation of an issue into a fully hydrated issue
        object, with the help of a timeline provider to fetch the events timeline."""
        repo = json_issue['repository_url'][29:]
        number = json_issue['number']
        title = json_issue['title']
        body = json_issue['body']
        created_at = dateutil.parser.parse(json_issue['created_at'])
        updated_at = dateutil.parser.parse(json_issue['updated_at'])
        closed_at = (dateutil.parser.parse(json_issue['closed_at'])
                     if json_issue['closed_at'] is not None else None)
        state = json_issue['state']
        labels = [label['name'] for label in json_issue['labels']]
        assignees = [assignee['login'] for assignee in json_issue['assignees']]
        timeline = [Event(json_event) for json_event in
                    timeline_provider.get_timeline(repo, number, updated_at)]

        return cls(repo, number, title, body, created_at, updated_at,
                   state, timeline, labels, assignees, closed_at, json_issue=json_issue)

    def __str__(self):
        return '%s, %s:%s' % (self.repo, self.number, self.title)
