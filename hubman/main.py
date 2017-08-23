from hubman.github import Github

gh = Github()
for issue in gh.issues(['lampholder/test_data'], 'is:open'):
    print 'ISSUE: ', issue
    for event in issue.timeline:
        print '    EVENT: ', event
