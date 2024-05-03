from flask import Flask, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

from helpers import login_required

import sqlite3

# Configure app
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# connect to database using sqlite3
def get_db():
    '''
    https://flask.palletsprojects.com/en/2.3.x/patterns/sqlite3/
    '''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('project.db')
        db.row_factory = sqlite3.Row
    return db

# initialise database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        g.pop('_database')

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    db = get_db()
    credentials = db.execute("SELECT credential_id, login_title, login_name, login_password FROM credentials where user_id = ?", (user_id,)).fetchall()
    return render_template("index.html", credentials=credentials)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            message = "Username required"
            return render_template("register.html", message=message, visibility="visible")
        elif not password:
            message = "Password required"
            return render_template("register.html", message=message, visibility="visible")
        elif not confirmation:
            message = "Confirmation required"
            return render_template("register.html", message=message, visibility="visible")

        if password != confirmation:
            message = "Passwords do not match"
            return render_template("register.html", message=message, visibility="visible")

        # Password validation
        if len(password) < 8:
            message = "Password should be at least 8 characters long."
            return render_template("register.html", message=message, visibility="visible")
        elif not any(char.isdigit() for char in password):
            message = "Password should contain at least one digit."
            return render_template("register.html", message=message, visibility="visible")
        elif not any(char.isalpha() for char in password):
            message = "Password should contain at least one letter."
            return render_template("register.html", message=message, visibility="visible")

        hash = generate_password_hash(password)

        try:
            # successful
            db = get_db()
            # now you can use get_db()
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, hash))
            db.commit()
            return redirect("/")
        except Exception as e:
            print("error:" + str(e))
            return render_template("register.html", message="Registration unsuccessful", visibility="visible")

    else:
        return render_template("register.html", visibility="invisible")
    

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":

        if not username:
            message = "Username required"
            return render_template("login.html", message=message, visibility="visible")

        # Ensure password was submitted
        elif not password:
            message = "Password required"
            return render_template("login.html", message=message, visibility="visible")

        # Query database for username
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", [username])
        user = user.fetchall()

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["password_hash"], request.form.get("password")):
            message = "Incorrect username or password"
            return render_template("login.html", message=message, visibility="visible")

        # Remember which user has logged in
        session["user_id"] = user[0]["user_id"]

        return redirect("/")

    else:
        return render_template("login.html", visibility="invisible")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    session["username"] = None
    return redirect("/")

@app.route("/generate", methods=["GET", "POST"])
@login_required
def generator():
    if request.method == "POST":
    #return render_template("generator.html")
    #if request.method == "POST":
        title = request.form.get("title")
        username = request.form.get("username")
        password = request.form.get("password")

        if not (title and username and password):
            return render_template("generator.html", message="Title, username and password cannot be empty.", visibility="visible")
        else:
            user_id = session["user_id"]
            db = get_db()
            db.execute("INSERT INTO credentials (user_id, login_title, login_name, login_password) values (?, ?, ?, ?)",
                       (user_id, title, username, password))
            db.commit()

    return render_template("generator.html", visibility="invisible")


@app.route("/updateCredential", methods=["POST"])
@login_required
def updateCredential():
    if request.method == "POST":
        title = request.form.get("titleInput")
        username = request.form.get("usernameInput")
        password = request.form.get("passwordInput")

        user_id = session["user_id"]  # Assuming user_id is stored in the session
        db = get_db()

        # Replace this SQL query with your actual update query
        db.execute("UPDATE credentials SET login_title = ?, login_name = ?, login_password = ? WHERE user_id = ?",
                   (title, username, password, user_id))
        db.commit()
        return redirect("/")
    else:
        return redirect("/")

@app.route("/deleteCredential", methods=["POST"])
@login_required
def deleteCredential():
    if request.method == "POST":
        credential_id = request.form.get("credentialId")
        user_id = session["user_id"]
        db = get_db()
        db.execute("DELETE FROM credentials WHERE credential_id = ? AND user_id = ?", (credential_id, user_id))
        db.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)