from utils.db_management.sqls import Queries
from psycopg2.errors import UniqueViolation
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import json
from clogger.clogger import CLogger

logger = CLogger.get('database')

POSTGRES_HOST = "postgresdb"
POSTGRES_PASSWORD = "password"
POSTGRES_USER = "postgres"


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(host=POSTGRES_HOST,
                                     password=POSTGRES_PASSWORD,
                                     user=POSTGRES_USER)
        self.cursor = self.conn.cursor()
        self.initialise_all_tables()
        self.engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/')
        logger.info('Initialised')

    def initialise_all_tables(self):
        self.execute(Queries.CREATE_USER_TABLE)
        self.execute(Queries.CREATE_PROJECT_TABLE)
        self.execute(Queries.CREATE_ACCESS_TABLE)

    def execute(self, query, data=""):
        try:
            self.cursor.execute(query, data)
            self.conn.commit()
            return 0, ""
        except UniqueViolation:
            self.conn.rollback()
            return 2, ""
        except Exception as e:
            print(e)
            self.conn.rollback()
            return 1, e

    def select(self, query):
        df = pd.read_sql(query, self.conn)
        return df
    
    def save_df(self, df, tablename):
        df.to_sql(tablename, self.engine, index=False, if_exists='replace')
    
    def get_user(self, username):
        command = f"SELECT username, password from users where username = '{username}'"
        df = self.select(command)
        if len(df):
            return df.to_dict(orient='index')[0]
        return {}



