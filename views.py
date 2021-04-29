from flask import (
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for,
    send_from_directory,
)
from models.game import Game
from models.user import User
from dao import GameDao, UserDao
from gameflix import app, db
from helpers.game_cover import delete_game_cover, get_game_cover, upload_game_cover

game_dao = GameDao(db)
user_dao = UserDao(db)


@app.route("/")
def index():
    game_list = game_dao.list()
    return render_template("index.html", title="Gameflix", games=game_list)


@app.route("/login")
def login():
    if "logged_user" in session and session["logged_user"]:
        return redirect(url_for("index"))
    next_page = request.args.get("next")
    return render_template("login/login.html", next=next_page, title="Login")


@app.route("/logout")
def logout():
    if "logged_user" in session:
        session["logged_user"] = None
        flash("User logged out")
    return redirect(url_for("index"))


@app.route(
    "/authenticate",
    methods=[
        "POST",
    ],
)
def authenticate():
    username = request.form["username"]
    user = user_dao.find_by_id(username)
    if user:
        if user.password == request.form["password"]:
            session["logged_user"] = user.id
            flash(user.name + " has logged in")
            next_page = request.form["next"]
            return redirect(next_page)

    flash("Login failed, try again")
    return redirect(url_for("login"))


@app.route("/new_game")
def new_game():
    if not session["logged_user"] or session["logged_user"] == None:
        return redirect(url_for("login", next=url_for("new_game")))

    return render_template("game/new_game.html", title="New Game")


@app.route("/edit_game/<int:id>")
def edit_game(id):
    if not session["logged_user"] or session["logged_user"] == None:
        return redirect(url_for("login", next=url_for("new_game")))

    game = game_dao.find_by_id(id)

    new_game_cover = get_game_cover(id)

    return render_template(
        "game/edit_game.html",
        title="Editing Game",
        game=game,
        game_cover=new_game_cover or "default.jpg",
    )


@app.route("/uploads/<file_name>")
def image(file_name):
    return send_from_directory(app.config["GAME_COVERS_UPLOAD_PATH"], file_name)


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
    game = game_dao.save(game)

    upload_game_cover(request.files["game_cover"], game.id)

    return redirect(url_for("index"))


@app.route(
    "/save_game",
    methods=[
        "POST",
    ],
)
def save_game():
    name = request.form["name"]
    category = request.form["category"]
    console = request.form["console"]

    game = Game(name, category, console, id=request.form["id"])

    game_cover = request.files["game_cover"]
    delete_game_cover(game.id)
    upload_game_cover(game_cover, game.id)

    game_dao.save(game)

    return redirect(url_for("index"))


@app.route("/delete_game/<int:id>")
def delete_game(id):
    game_dao.delete(id)
    delete_game_cover(id)
    flash("Game deleted!")
    return redirect(url_for("index"))