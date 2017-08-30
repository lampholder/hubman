from hubman.github import Github
from hubman.github import Query

from requests.auth import HTTPBasicAuth

from datetime import datetime

with open('token', 'r') as token_file:
    token = token_file.read().strip()

auth = HTTPBasicAuth('lampholder', token)

gh = Github(auth)
#for issue in gh.issues(['lampholder/test_data'], 'is:open'):
#    print 'ISSUE: ', issue
#    for event in issue.timeline:
#        print '    EVENT: ', event

repos = ['lampholder/test_data']

print 'FEATURE BACKLOG:'
query = Query('is:open no:assignee label:feature -label:"ready to start"')
feature_backlog = gh.issues(repos, query)
for issue in feature_backlog:
    print issue,
    while query.matches(issue):
        timestamp = issue.timeline[-1].timestamp
        issue = issue.rollback()
    print datetime.now(timestamp.tzinfo) - timestamp

print

print 'READY TO START:'
query = Query('is:open no:assignee label:feature label:"ready to start"')
ready_to_start = gh.issues(repos, query)
for issue in ready_to_start:
    print issue,
    while query.matches(issue):
        timestamp = issue.timeline[-1].timestamp
        issue = issue.rollback()
    print datetime.now(timestamp.tzinfo) - timestamp
print

# FIXME: This won't work yet.
print 'IN FLIGHT:'
query = Query('is:open label:feature')
in_flight = [issue for issue in gh.issues(repos, query) if len(issue.assignees) > 0]
for issue in in_flight:
    print issue,
    while query.matches(issue):
        timestamp = issue.timeline[-1].timestamp
        issue = issue.rollback()
    print datetime.now(timestamp.tzinfo) - timestamp
print

"""
print 'IN REVIEW:'
print 'Mentioned in a PR that is not yet merged.'
print

print 'REVIEW COMPLETE:'

"""
"""
Types of querier:
    - added to every query string
    - fork the original query string
    - filter after the event (applied to all forks)


    (label:feature and label:p1) or label:bug
     -----.-> label:feature label:p1
          |
          .-> label:bug

    is:open x or y == is:open and (x or y)
"""


