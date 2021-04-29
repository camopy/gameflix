from gameflix import app
import os
import time


def upload_game_cover(game_cover, game_id):
    game_covers_upload_path = app.config["GAME_COVERS_UPLOAD_PATH"]
    timestamp = time.time()
    game_cover.save(f"{game_covers_upload_path}/cover{game_id}-{timestamp}.jpg")


def get_game_cover(id):
    for file_name in os.listdir(app.config["GAME_COVERS_UPLOAD_PATH"]):
        if f"cover{id}" in file_name:
            return file_name


def delete_game_cover(id):
    game_cover = get_game_cover(id)
    os.remove(os.path.join(app.config["GAME_COVERS_UPLOAD_PATH"], game_cover))