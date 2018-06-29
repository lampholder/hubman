import sys

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

repos = ['vector-im/riot-web', 'matrix-org/matrix-js-sdk',
         'matrix-org/matrix-react-sdk']
order = ['BACKLOG', 'IN PROGRESS', 'IN REVIEW', 'DONE']
board = {
            'BACKLOG': Query('is:issue is:open milestone:RW010 no:assignee'),
            'IN PROGRESS': Query('is:issue is:open is:assigned'),
            'AWAITING REVIEW': Query('is:pr is:open -is:assigned'),
            'IN REVIEW': Query('is:pr is:open is:assigned'),
            'DONE': Query('is:issue is:closed project:vector-im/riot-web/9')
        }
def chunkstring(string, length):
        return (string[0+i:length+i] for i in range(0, len(string), length))




def render_column(heading, repos, query):
    print '%s:' % heading
    issues = gh.issues(repos, query)
    for issue in issues:
        print '.---------------------------------.'
        print '| {: <31} |'.format(issue.repo)
        print '| #{: <30} |'.format(issue.number)
        for chunk in chunkstring(issue.title, 31):
            print '| {:31.31} |'.format(chunk)
        print '|                                 |'
        while query.matches(issue) and len(issue.timeline) > 0:
            timestamp = issue.timeline[-1].timestamp
            issue = issue.rollback()
        time_in_state = datetime.now(timestamp.tzinfo) - timestamp
        print '| {:>31.31} |'.format(time_in_state)
        print '._________________________________.'
    print

column = sys.argv[1]

render_column(column, repos, board[column])
