
class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ''
    MYSQL_DB = "revision_tecnica"


config = {
    "development": DevelopmentConfig
}