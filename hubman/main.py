from datetime import datetime
from requests.auth import HTTPBasicAuth
from hubman.github import Github
from hubman.github import Query

with open('token', 'r') as token_file:
    token = token_file.read().strip()

auth = HTTPBasicAuth('lampholder', token)

gh = Github(auth)

#repos = ['lampholder/test_data']
#order = ['FEATURE BACKLOG', 'READY TO START', 'IN FLIGHT']
#board = {'FEATURE BACKLOG': Query('is:open no:assignee label:feature -label:"ready to start"'),
#         'READY TO START': Query('is:open no:assignee label:feature label:"ready to start"'),
#         'IN FLIGHT': Query('is:open label:feature is:assigned')}

repos = ['vector-im/riot-web']
order = ['BACKLOG', 'READY TO START', 'IN PROGRESS', 'DONE']
board = {
            'BACKLOG': Query('is:issue is:open project:vector-im/riot-web/9 no:assignee -label:"ready to start"'),
            'READY TO START': Query('is:issue is:open project:vector-im/riot-web/9 no:assignee label:"ready to start"'),
            'IN PROGRESS': Query('is:issue is:open project:vector-im/riot-web/9 is:assigned'),
            'DONE': Query('is:issue is:closed project:vector-im/riot-web/9')
        }


def render(repos, board, order):
    for status in order:
        query = board[status]
        print '%s:' % status
        issues = gh.issues(repos, query)
        for issue in issues:
            print issue.number, issue.title,
            while query.matches(issue) and len(issue.timeline) > 0:
                timestamp = issue.timeline[-1].timestamp
                issue = issue.rollback()
            print datetime.now(timestamp.tzinfo) - timestamp
        print

render(repos, board, order)
