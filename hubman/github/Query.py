"""Query.py"""
import re

class Query(object):
    """Class to handle both simple query entites and complex ones."""

    def __init__(self, query_string):
        self.query_string = query_string

    def _get_tagged_query_params(self, tag,
                                 positive_constructor,
                                 negative_constructor):
        positive_regex = r'[^-]%s:(\w+|"(?:[^"\\]|\\.)*")' % tag
        negative_regex = r'-%s:(\w+|"(?:[^"\\]|\\.)*")' % tag

        positive = set([positive_constructor(label[1:-1])
                        if label[0] == '"' else positive_constructor(label)
                        for label in re.findall(positive_regex,
                                                self.query_string)])
        negative = set([negative_constructor(label[1:-1])
                        if label[0] == '"' else negative_constructor(label)
                        for label in re.findall(negative_regex,
                                                self.query_string)])
        return positive.union(negative)

    def get_labels(self):
        return self._get_tagged_query_params('label', PositiveLabelQuery,
                                             NegativeLabelQuery)

    def get_assignees(self):
        return self._get_tagged_query_params('assignee', PositiveAssigneeQuery,
                                             NegativeAssigneeQuery)

    def get_assigned(self):
        positive_assigned_regex = r'[^-]is:assigned\b'
        negative_assigned_regex = r'-is:assigned\b'

        query_components = []

        # N.B. this is designed to let people put both is:assigned and -is:assigned
        # in the same query. It's not our job to police the query, and this way it
        # should fail sooner and more obviously.
        if re.search(positive_assigned_regex, self.query_string) is not None:
            query_components += PositiveAssignedQuery()

        if re.search(negative_assigned_regex, self.query_string) is not None:
            query_components += NegativeAssignedQuery()

        return query_components

    def to_github_query_string(self):
        return (self.query_string
                .replace('-is:assigned', 'unassigned')
                .replace('is:assigned', ''))

    def matches(self, issue):
        for label in self.get_labels():
            if not label.matches(issue):
                return False
        for assignee in self.get_assignees():
            if not assignee.matches(issue):
                return False
        for assigned in self.get_assigned():
            if not assigned.matches(issue):
                return False
        return True

class PositiveAssignedQuery(object):
    """Query object representing an Issue's being assigned to _someone_."""

    @staticmethod
    def is_positive():
        """Returns True to show that this is a positive query element (i.e. we
        match when the entity represented is _present_ rather than absent.)"""
        return True

    @staticmethod
    def matches(issue):
        """Matches if there are any assignees."""
        return len(issue.assignees) > 0

class NegativeAssignedQuery(object):
    """Query object representing an Issue's being assigned to _nobody_."""

    @staticmethod
    def is_positive():
        """Returns False to show that this is a negative query element (i.e. we
        match when the entity represented is absent.)"""
        return False

    @staticmethod
    def matches(issue):
        """Matches if there are no assignees."""
        return len(issue.assignees) == 0

class PositiveLabelQuery(object):
    """Query object representing an Issue's having a certain label present"""

    def __init__(self, label):
        self.label = label

    @staticmethod
    def is_positive():
        """Returns True to show that this is a positive query element (i.e. we
        match when the entity represented is _present_ rather than absent.)"""
        return True

    def matches(self, issue):
        """Returns True if this query component matches the Issue state."""
        return self.label in issue.labels

    def __str__(self):
        return 'label:%s' % self.label

    def __repr__(self):
        return self.__str__()

class NegativeLabelQuery(object):
    """Query object representing an Issue's _not_ having a certain label present"""

    def __init__(self, label):
        self.label = label

    @staticmethod
    def is_positive():
        """Returns False to show that this is a negative query element (i.e. we
        match when the entity represented is absent.)"""
        return False

    def matches(self, issue):
        """Returns True if this query component matches the Issue state."""
        return self.label not in issue.labels

    def __str__(self):
        return '-label:%s' % self.label

    def __repr__(self):
        return self.__str__()

class PositiveAssigneeQuery(object):
    """Query object representing an Issue's having a certain assignee present"""

    def __init__(self, assignee):
        self.assignee = assignee

    @staticmethod
    def is_positive():
        """Returns True to show that this is a positive query element (i.e. we
        match when the entity represented is _present_ rather than absent.)"""
        return True

    def matches(self, issue):
        """Returns True if this query component matches the Issue state."""
        return self.assignee in issue.assignees

class NegativeAssigneeQuery(object):
    """Query object representing an Issue's _not_ having a certain assignee present"""

    def __init__(self, assignee):
        self.assignee = assignee

    @staticmethod
    def is_positive():
        """Returns False to show that this is a negative query element (i.e. we
        match when the entity represented is absent.)"""
        return False

    def matches(self, issue):
        """Returns True if this query component matches the Issue state."""
        return self.assignee not in issue.assignee
