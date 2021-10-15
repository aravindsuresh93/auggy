from utils.db_management.sqls import Queries
from psycopg2.errors import UniqueViolation
import pandas as pd
import psycopg2
import json

POSTGRES_HOST = "0.0.0.0"
POSTGRES_PASSWORD = "password"
POSTGRES_USER = "postgres"


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(host=POSTGRES_HOST,
                                     password=POSTGRES_PASSWORD,
                                     user=POSTGRES_USER)
        self.cursor = self.conn.cursor()
        self.initialise_all_tables()

    def execute(self, query):
        """
        Execute a query
        """
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, query, data):
        """
        Execute insert query
        """
        self.cursor.execute(query, data)
        self.conn.commit()

    def select(self, query):
        """
        Run select query
        """
        df = pd.read_sql(query, self.conn)
        return df

    def delete_table(self):
        self.execute(Queries.DROP_TABLE)

    def initialise_all_tables(self):
        self.execute(Queries.CREATE_USER_TABLE)
        self.execute(Queries.CREATE_PROJECT_TABLE)

    def close(self):
        self.conn.close()

    def create_user(self, username, password):
        try:
            self.insert(Queries.ADD_USER, (username, password, json.dumps({})))
            return 0, f"Registered {username}"
        except UniqueViolation:
            self.conn.rollback()
            return 1, "User already exists"
        except Exception as e:
            self.conn.rollback()
            return 1, e

    def get_user(self, username):
        command = f"SELECT username, password from users where username = '{username}'"
        df = self.select(command)
        if len(df):
            return df.to_dict(orient='index')[0]
        return {}






db = DB()
# db.add_user("aravind", "pass")
# db.delete_table()
# df = db.query("select * from users")
# df = db.get_user("aravind1")
# print(df)
