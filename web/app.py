from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask.globals import g
from flask import session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import sqlite3
import datetime

# from flask_mysqldb import MySQL
# from flask_socketio import SocketIO, emit


app = Flask(__name__)
# socketio = SocketIO(app)
app.secret_key = "your_secret_key_here"


login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


users = {"user1": {"password": "password1"}}

# Define the SQLite database file
DB_FILE = "words.db"


# Function to establish a database connection
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
    return db


# Create the table if it doesn't exist
with app.app_context():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Words (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Word TEXT NOT NULL,
            Extra TEXT,
            Wrong_posibilities TEXT,
            date_create DATETIME NOT NULL,
            date_update DATETIME
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    db.commit()


# Teardown function to close the database connection when the request is done
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        word = request.form["Word"]
        extra = request.form["Extra"]
        wrong_posibilities = request.form["Wrong_posibilities"]
        date_create = datetime.datetime.now()
        date_update = None

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO Words (Word, Extra, Wrong_posibilities, date_create, date_update)
            VALUES (?, ?, ?, ?, ?)
        """,
            (word, extra, wrong_posibilities, date_create, date_update),
        )
        db.commit()

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Words ORDER BY date_create DESC")
    words = cursor.fetchall()

    return render_template("index.html", words=words)


@app.route("/words")
@login_required
def words():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Words ORDER BY date_create DESC")
    words = cursor.fetchall()
    return render_template("words.html", words=words)


@app.route("/delete/<int:word_id>")
@login_required
def delete_word(word_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Words WHERE ID = ?", (word_id,))
    word = cursor.fetchone()

    if word is None:
        # Word with the specified ID was not found
        flash("Word not found.", "danger")
    else:
        # Word found, delete it
        cursor.execute("DELETE FROM Words WHERE ID = ?", (word_id,))
        db.commit()
        flash("Word deleted successfully.", "success")

    return redirect(url_for("words"))


@app.route("/edit/<int:word_id>", methods=["GET", "POST"])
@login_required
def edit_word(word_id):
    db = get_db()
    cursor = db.cursor()
    if request.method == "POST":
        # Handle form submission for updating the Word
        word = request.form["Word"]
        extra = request.form["Extra"]
        wrong_posibilities = request.form["Wrong_posibilities"]
        date_update = datetime.datetime.now()

        cursor.execute(
            "UPDATE Words SET Word = ?, Extra = ?, Wrong_posibilities = ?, date_update = ? WHERE ID = ?",
            (word, extra, wrong_posibilities, date_update, word_id),
        )
        db.commit()
        flash("Word updated successfully.", "success")
        return redirect(url_for("words"))

    cursor.execute("SELECT * FROM Words WHERE ID = ?", (word_id,))
    word = cursor.fetchone()

    if word is None:
        flash("Word not found.", "danger")
        return redirect(url_for("words"))

    return render_template("edit_word.html", word=word)


@app.route("/add_word", methods=["GET", "POST"])
@login_required
def add_word():
    if request.method == "POST":
        # Handle form submission for adding a new Word
        word = request.form["Word"]
        extra = request.form["Extra"]
        wrong_posibilities = request.form["Wrong_posibilities"]
        date_create = datetime.datetime.now()
        date_update = None

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO Words (Word, Extra, Wrong_posibilities, date_create, date_update)
            VALUES (?, ?, ?, ?, ?)
        """,
            (word, extra, wrong_posibilities, date_create, date_update),
        )
        db.commit()

        flash("Word added successfully.", "success")
        return redirect(url_for("words"))

    return render_template("add_word.html")


@app.route("/search")
def search():
    search_query = request.args.get("search_query", "").strip().lower()

    if search_query:
        # Query the database for words that match the search query
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT * FROM Words
            WHERE lower(Word) LIKE ? OR lower(Extra) LIKE ? OR lower(Wrong_posibilities) LIKE ?
        """,
            (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"),
        )
        search_results = cursor.fetchall()
    else:
        # If no search query provided, return all Words
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Words")
        search_results = cursor.fetchall()

    return render_template(
        "index.html", search_results=search_results, search_query=search_query
    )


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("index"))

        flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("index"))


@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == "POST":
        sender = request.form["sender"]
        message = request.form["message"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO messages (sender, message) VALUES (?, ?)", (sender, message)
        )
        db.commit()

    try:
        # Fetch existing messages from the database

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM messages ORDER BY timestamp desc LIMIT 100")
        messages = cursor.fetchall()
        # print(messages)
    except sqlite3.Error as e:
        print("SQLite error:", e)
        messages = []

    return render_template("chat.html", messages=messages)
    # return render_template("chat.html")


@app.route("/get_messages")
def get_messages():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM messages ORDER BY timestamp desc LIMIT 1000")
        messages = cursor.fetchall()
        # print(messages)
    except sqlite3.Error as e:
        print("SQLite error:", e)
        messages = []
    return jsonify(messages)


# @socketio.on("message")
# def handle_message(message):
#     print("message", message)
#     sender = message["sender"]
#     message = message["message"]

#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute(
#         "INSERT INTO messages (sender, message) VALUES (?, ?)", (sender, message)
#     )
#     db.commit()
#     # Broadcast the new message to all connected clients

#     now = datetime.datetime.now()
#     formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
#     socketio.emit(
#         "new_message",
#         {"message": message, "sender": sender, "datetime": formatted_date},
#     )


# @socketio.on("connect")
# def handle_connect():
#     print("Client connected")


# @socketio.on("disconnect")
# def handle_disconnect():
#     print("Client disconnected")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # , debug=True
