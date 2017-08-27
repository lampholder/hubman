from hubman.github import Github
from hubman.github import Query

from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('lampholder', 'f6858c65176eba89b76c9d8a384461c540c5ca1b')

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
    print issue, query.matches(issue)
    #for event in issue.timeline:
    #    print '  EVENT: ', event
print

"""
print 'READY TO START:'
ready_to_start = gh.issues(repos, 'is:open no:assignee label:feature label:"ready to start"')
for issue in ready_to_start:
    print issue
    for event in issue.timeline:
        print '  EVENT: ', event
print

print 'IN FLIGHT:'
in_flight = [issue for issue in gh.issues(repos, 'is:open label:feature') if len(issue.assignees) > 0]
for issue in in_flight:
    print issue
    for event in issue.timeline:
        print '  EVENT: ', event
print

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


