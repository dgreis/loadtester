from settings import SETTINGS

import pymysql
import pandas as pd

class DB(object):

    def __init__(self):
        query_contents = None

    def _assemble_db_kwargs(self):
        dbc_keys = filter(lambda k: 'DBC' in k, SETTINGS)
        dbc_kwargs = dict()
        for k in dbc_keys:
            dbc_kwargs[k.split('DBC_')[1].lower()] = SETTINGS[k]
        return dbc_kwargs

    def execute_query(self, query):
        dbc_kwargs = self._assemble_db_kwargs()
        conn = pymysql.connect(**dbc_kwargs)
        contents = pd.read_sql(query, conn)
        self.query_contents = contents