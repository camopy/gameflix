from models.game import Game
from models.user import User

SQL_DELETE_GAME = "delete from game where id = %s"
SQL_GAME_BY_ID = "SELECT id, name, category, console from game where id = %s"
SQL_UPDATE_GAME = "UPDATE game SET name=%s, category=%s, console=%s where id = %s"
SQL_FIND_ALL_GAMES = "SELECT id, name, category, console from game"
SQL_CREATE_GAME = "INSERT into game (name, category, console) values (%s, %s, %s)"
SQL_USER_BY_ID = "SELECT id, name, password from user where id = %s"


class UserDao:
    def __init__(self, db):
        self.__db = db

    def find_by_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USER_BY_ID, (id,))
        data = cursor.fetchone()
        user = translate_user(data) if data else None
        return user


def translate_user(user_data):
    return User(user_data[0], user_data[1], user_data[2])


class GameDao:
    def __init__(self, db):
        self.__db = db

    def save(self, game):
        cursor = self.__db.connection.cursor()

        if game.id:
            cursor.execute(
                SQL_UPDATE_GAME, (game.name, game.category, game.console, game.id)
            )
        else:
            cursor.execute(SQL_CREATE_GAME, (game.name, game.category, game.console))
            game.id = cursor.lastrowid
        self.__db.connection.commit()
        return game

    def list(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_FIND_ALL_GAMES)
        games = translate_games(cursor.fetchall())
        return games

    def find_by_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_GAME_BY_ID, (id,))
        game_data = cursor.fetchone()
        return Game(game_data[1], game_data[2], game_data[3], id=game_data[0])

    def delete(self, id):
        self.__db.connection.cursor().execute(SQL_DELETE_GAME, (id,))
        self.__db.connection.commit()


def translate_games(games):
    def create_game_from_tuple(game_data):
        return Game(game_data[1], game_data[2], game_data[3], id=game_data[0])

    return list(map(create_game_from_tuple, games))