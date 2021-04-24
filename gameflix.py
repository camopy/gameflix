from flask import Flask, render_template, request, redirect, session, flash, url_for
from game import Game
from user import User

app = Flask(__name__)
app.secret_key = "gameflix"

tetris = Game("Tetris", "Arcade", "Megadrive")
mario = Game("Super Mario", "Action", "SNES")
pokemon = Game("Pokemon Gold", "RPG", "GBA")
games = [tetris, mario, pokemon]

paulo = User("paulo", "Paulo", "123")
amanda = User("amanda", "Amanda", "321")
users = {paulo.id: paulo, amanda.id: amanda}


@app.route("/")
def index():
    return render_template("index.html", title="Gameflix", games=games)


@app.route("/login")
def login():
    next_page = request.args.get("next")
    return render_template("login/login.html", next=next_page, title="Login")


@app.route("/logout")
def logout():
    session["logged_user"] = None
    flash("User not logged in")
    return redirect(url_for("index"))


@app.route(
    "/authenticate",
    methods=[
        "POST",
    ],
)
def authenticate():
    username = request.form["username"]
    if username in users:
        user = users[username]
        if user.password == request.form["password"]:
            session["logged_user"] = user.id
            flash(user.name + " has logged in")
            next_page = request.form["next"]
            return redirect(next_page)

    flash("Login failed, try again")
    return redirect(url_for("login"))


@app.route("/new_game")
def new_game():
    if not session["logged_user"]:
        return redirect(url_for("login", next=url_for("new_game")))

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
    return redirect(url_for("index"))


app.run(debug=True)
