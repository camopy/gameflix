from flask import Flask, render_template, request, redirect, session, flash
from game import Game

app = Flask(__name__)
app.secret_key = "gameflix"

tetris = Game("Tetris", "Arcade", "Megadrive")
mario = Game("Super Mario", "Action", "SNES")
pokemon = Game("Pokemon Gold", "RPG", "GBA")
games = [tetris, mario, pokemon]


@app.route("/")
def index():
    return render_template("index.html", title="Gameflix", games=games)


@app.route("/login")
def login():
    return render_template("login/login.html", title="Login")


@app.route("/logout")
def logout():
    session["logged_user"] = None
    flash("User not logged in")
    return redirect("/")


@app.route(
    "/authenticate",
    methods=[
        "POST",
    ],
)
def authenticate():
    if "master" == request.form["password"]:
        user = request.form["username"]
        session["logged_user"] = user
        flash(user + " has logged in")
        return redirect("/")
    else:
        flash("Login failed, try again")
        return redirect("/login")


@app.route("/new_game")
def new_game():
    if not session["logged_user"]:
        return redirect("/login")

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
