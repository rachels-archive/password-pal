from flask import Flask, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

import sqlite3

# Configure app
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# helper functions
# decorate routes to require login.
def login_required(f):
    """
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# connect to database using sqlite3
def get_db():
    '''
    https://flask.palletsprojects.com/en/2.3.x/patterns/sqlite3/
    '''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
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
    return render_template("index.html")

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
        if len(user) != 1 or not check_password_hash(user[0]["hash"], request.form.get("password")):
            message = "Incorrect username or password"
            return render_template("login.html", message=message, visibility="visible")

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html", visibility="invisible")
    

@app.route("/logout")
def logout():
    session.clear()
    session["username"] = None
    return redirect("/")

@app.route("/generator", methods=["GET", "POST"])
def generator():
    return render_template("generator.html")

if __name__ == '__main__': 
    app.run(debug=True)