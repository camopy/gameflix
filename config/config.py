import os

SECRET_KEY = "gameflix"

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../uploads"
GAME_COVERS_UPLOAD_PATH = f"{UPLOAD_PATH}/game_covers"

MYSQL_HOST = "localhost"
MYSQL_USER = "camopy"
MYSQL_PASSWORD = "devdb"
MYSQL_DB = "gameflix"
MYSQL_PORT = 3306