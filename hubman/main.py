from hubman.github import Github

from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('lampholder', 'e129537f18451cfe1654833aed503b8a55c9e742')

gh = Github(auth)
#for issue in gh.issues(['lampholder/test_data'], 'is:open'):
#    print 'ISSUE: ', issue
#    for event in issue.timeline:
#        print '    EVENT: ', event

repos = ['lampholder/test_data']

print 'FEATURE BACKLOG:'
feature_backlog = gh.issues(repos, 'is:open no:assignee label:feature -label:"ready to start"')
for issue in feature_backlog:
    print issue
    for event in issue.timeline:
        print '  EVENT: ', event
print

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
