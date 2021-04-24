from flask import Flask, render_template, request, redirect
from game import Game

app = Flask(__name__)

tetris = Game("Tetris", "Arcade", "Megadrive")
mario = Game("Super Mario", "Action", "SNES")
pokemon = Game("Pokemon Gold", "RPG", "GBA")
games = [tetris, mario, pokemon]


@app.route("/")
def index():
    return render_template("index.html", title="Gameflix", games=games)


@app.route("/new_game")
def new_game():
    return render_template("game/new_game.html", title="New Game")


@app.route(
    "/create_game",
    methods=[
        "POST",
    ],
)
def create_game():
    name = request.form["name"]
    category = request.form["category"]
    console = request.form["console"]

    game = Game(name, category, console)
    games.append(game)
    return redirect("/")


app.run(debug=True)
