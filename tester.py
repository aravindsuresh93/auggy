from utils.db_management.db_connector import DB
from utils.db_management.sqls import Queries
db =DB()
db.execute(Queries.DROP_TABLES)
df = db.select(Queries.SHOW_ALL_TABLES, )
print(df)