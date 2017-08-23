"""IssueFetcher.py"""
import requests

from hubman.github import GithubClient

class IssueFetcher(GithubClient):
    """Responsible for pulling JSON representations of issues back from Github. It's
    somebody else's job to dress that JSON up nicely."""

    @classmethod
    def fetch(cls, repos, query, auth):
        """A generator that pulls all of the matching issues (in JSON) from Github"""

        #Github strongly encourages this:
        headers = {'Accept': 'application/vnd.github.v3+json'}

        search_url = cls._url + '/search/issues'
        params = {'q': ' '.join(['repo:%s' % repo for repo in repos]) + ' ' + query}

        github_response = requests.get(search_url, headers=headers, params=params, auth=auth)

        def issue_fetcher(response_json):
            """Custom fetching strategy - yeild everything in the 'items'
            array, one by one."""
            for json_entity in response_json['items']:
                yield json_entity

        return cls.drain(github_response, headers=headers, auth=auth,
                         fetcher=issue_fetcher)
