from decouple import config

class Settings:
    """Configuration settings for database connection."""
    user: str = config("db_user")
    password: str = config("db_password")
    host: str = config("db_host")
    port: str = config("db_port")
    dbname: str = config("db_name")