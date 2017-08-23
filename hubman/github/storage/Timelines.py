"""Timelines.py"""
import json

from hubman.github.storage import Store

class Timelines(Store):
    """Class to represent persistent storage of timelines cache"""

    table_name = 'timelines'
    schema = \
        """
        drop table if exists %s;
        create table %s (
            repo string not null,
            issue_number number not null,
            freshness string not null,
            timeline string not null,
            constraint repo_issue unique(repo, issue_number)
        );
        """ % (table_name, table_name)

    def __init__(self):
        self._load_schema_if_necessary()

    def row_to_entity(self, row, connection):
        return row

    def fetch(self, repo, issue_number, freshness, connection):
        """Fetch the cached timeline (if it is fresh enough)"""
        sql = ('select * from timelines where repo = ? and issue_number = ? and ' +
               'freshness >= ?')
        cursor = connection.execute(sql, (repo, issue_number, freshness, ))
        return self.one_or_none(cursor)

    def create(self, repo, issue_number, freshness, json_timeline, connection):
        """Insert the latest cached timeline, erasing an old cached instance if it
        exists"""
        sql = 'delete from timelines where repo = ? and issue_number = ?'
        connection.execute(sql, (repo, issue_number, ))
        sql = ('insert into timelines(repo, issue_number, freshness, timeline) values ' +
               '(?, ?, ?, ?)')
        cursor = connection.execute(sql, (repo, issue_number, freshness, json_timeline, ))
        insert_id = cursor.lastrowid
        cursor.close()
        return insert_id
