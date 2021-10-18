class Queries:
    """
    Wraps all sql queries
    """
    """
    Table management
    """
    DROP_TABLES = "DROP TABLE users, projects, access"
    CREATE_USER_TABLE = "CREATE TABLE IF NOT EXISTS users (username VARCHAR PRIMARY KEY, password VARCHAR, info JSONB)"
    CREATE_PROJECT_TABLE = "CREATE TABLE IF NOT EXISTS projects (projectname VARCHAR PRIMARY KEY, metainfo JSONB, info JSONB)"
    CREATE_ACCESS_TABLE = "CREATE TABLE IF NOT EXISTS access (username VARCHAR, projectname VARCHAR, access VARCHAR, PRIMARY KEY (username, projectname)) "

    """
    User Management
    """
    CREATE_USER = "INSERT INTO USERS VALUES (%s, %s, %s)"

    """
    Project Management
    """
    CREATE_PROJECT = "INSERT INTO PROJECTS VALUES (%s, %s, %s)"
    DELETE_PROJECT = "DELETE FROM PROJECTS WHERE projectname = %s"

    """
    Insert Access
    """
    INSERT_ACCESS = "INSERT INTO ACCESS VALUES (%s, %s, %s)"
    DELETE_ACCESS = "DELETE FROM ACCESS WHERE username = %s and projectname = %s"

