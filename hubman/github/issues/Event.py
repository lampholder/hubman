"""Event.py"""
from enum import Enum

import dateutil.parser

class Polarity(Enum):
    """Represents direction of event entity (labeled is ADDED, unlabeled is REMOVED"""
    ADDED = 'added'
    REMOVED = 'removed'

class Entity(Enum):
    """Represents the entity upon which an event is acting."""
    LABEL = 'label'
    ASSIGNEE = 'assignee'
    OPEN = 'open'
    IGNORED = 'ignored'

class Event(object):
    """Represents a github issue event."""

    def __init__(self, json_event):
        self.event_type = json_event['event']
        self.timestamp = dateutil.parser.parse(json_event['created_at'])

        (self.entity, self.polarity) = self.get_entity_and_polarity(self.event_type)

        self.payload = self.extract_payload(self.entity, json_event)

        self._json = json_event


    @staticmethod
    def extract_payload(entity, json_event):
        """Different events (labels, assignements, comments, etc.) have their own unique
        properties - this is an attempt to hammer that uniqueness into a homogenous shape."""
        if entity == Entity.LABEL:
            return json_event['label']['name']
        elif entity == Entity.ASSIGNEE:
            return json_event['assignee']['login']
        elif entity == Entity.OPEN:
            return 'open' if json_event['event'] == 'reopened' else 'closed'
        else:
            return None

    @staticmethod
    def get_entity_and_polarity(event_type):
        """Translates an event into an entity and polarity (+ve means applied, -ve
        means unapplied."""
        event_map = {'labeled': (Entity.LABEL, Polarity.ADDED),
                     'unlabeled': (Entity.LABEL, Polarity.REMOVED),
                     'assigned': (Entity.ASSIGNEE, Polarity.ADDED),
                     'unassigned': (Entity.ASSIGNEE, Polarity.REMOVED),
                     'closed': (Entity.OPEN, Polarity.REMOVED),
                     'reopened': (Entity.OPEN, Polarity.ADDED)}

        if event_type in event_map:
            return event_map[event_type]
        else:
            return (Entity.IGNORED, None)

    def __str__(self):
        return '%s: %s %s %s' % (self.timestamp, self.entity, self.polarity, self.payload)

    def __repr__(self):
        return self.__str__()
