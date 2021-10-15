class Queries:
    """
    Wraps all sql queries
    """
    """
    Table management
    """
    DROP_TABLE = "DROP TABLE users"
    CREATE_USER_TABLE = "CREATE TABLE IF NOT EXISTS users (username VARCHAR PRIMARY KEY, password VARCHAR, info JSONB)"
    CREATE_PROJECT_TABLE = "CREATE TABLE IF NOT EXISTS projects (projectname VARCHAR PRIMARY KEY, metainfo VARCHAR, info JSONB)"

    """
    User Management
    """
    ADD_USER = "INSERT INTO USERS VALUES (%s, %s, %s)"

    """
    Project Management
    """
