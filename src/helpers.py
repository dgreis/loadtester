from settings import SETTINGS

import pymysql
import pandas as pd

class Container(object):

    def __init__(self, backend, backend_args):
        self.backend = backend
        self.backend_args = backend_args
        self.contents = None

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
        return contents

    def gather_contents(self):
        backend = self.backend
        if backend == 'database':
            query = self.backend_args['PRODUCT_ALIAS_QUERY']
            contents = self.execute_query(query)
        elif backend == 'file':
            fileloc = self.backend_args['PRODUCT_FILE_LOC']
            contents = pd.read_csv(fileloc).reset_index()[['index', 'Handle']]
        self.contents = contents