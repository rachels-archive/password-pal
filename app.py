import sqlite3
from flask import Flask, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)
app.secret_key = "wkdw9123laqsk_!*#"

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    #user_id = session["user_id"]
    #data = get_db()
    db = get_db_connection()
    data = db.execute('SELECT * from users')
    return render_template('index.html', all_data = data)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # Establish connection with database
        db = g._database = sqlite3.connect('database.db')
        # cursor object that executes sql object
        cursor = db.cursor()
        cursor.execute("SELECT * from users")
        all_data = cursor.fetchall()
        all_data = [str(val) for val in all_data]
    # return result of execute command
    return all_data

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
if __name__ == '__main__':
    app.run()


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a p\ via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Username is required.")
        elif not password:
            return apology("Password is required.")
        elif not confirmation:
            return apology("Confirmation is required.")
        elif password != confirmation:
            return apology("Passwords do not match.")

        hashval = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashval)
            return redirect("/")
        except:
            return apology("User has already registered")

    else:

        return render_template("register.html")
