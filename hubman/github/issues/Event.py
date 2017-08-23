"""Event.py"""
import dateutil.parser

class Event(object):
    """Represents a github issue event."""

    def __init__(self, event_type, timestamp, json_event=None):
        self.event_type = event_type
        self.timestamp = timestamp
        self._json = json_event

    @classmethod
    def from_json(cls, json_event):
        """Translates a JSON representation of an event into the appropriate
        object representation."""
        event_type = json_event['event']
        timestamp = dateutil.parser.parse(json_event['created_at'])

        if event_type == 'labeled':
            label = json_event['label']['name']
            return LabeledEvent(event_type, timestamp, label, json_event)
        elif event_type == 'assigned':
            assignee = json_event['assignee']['login']
            return AssignedEvent(event_type, timestamp, assignee, json_event)
        elif event_type == 'commented':
            comment = json_event['body']
            return AssignedEvent(event_type, timestamp, comment, json_event)
        else:
            return Event(event_type, timestamp, json_event)

    def __str__(self):
        return '%s: %s' % (self.timestamp, self.event_type)


#TODO: All of these chaps can be handled with the same class (for now at least).

class AssignedEvent(Event):
    """Specific event class for Assigned event."""

    def __init__(self, event_type, timestamp, assignee, json_event=None):
        super(AssignedEvent, self).__init__(event_type, timestamp, json_event)
        self.assignee = assignee

    def __str__(self):
        return '%s: %s->%s' % (self.timestamp, self.event_type, self.assignee)

class LabeledEvent(Event):
    """Specific event class for Labeled event."""

    def __init__(self, event_type, timestamp, label, json_event=None):
        super(LabeledEvent, self).__init__(event_type, timestamp, json_event)
        self.label = label

    def __str__(self):
        return '%s: %s->%s' % (self.timestamp, self.event_type, self.label)

class CommentedEvent(Event):
    """Specific event class for Labeled event."""

    def __init__(self, event_type, timestamp, comment, json_event=None):
        super(CommentedEvent, self).__init__(event_type, timestamp, json_event)
        self.comment = comment

    def __str__(self):
        return '%s: %s->%s' % (self.timestamp, self.event_type, self.comment)
