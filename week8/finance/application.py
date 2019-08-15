import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    data = {}
    user_id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)[0]["cash"]
    posessions = db.execute("SELECT * FROM posessions WHERE id = :user_id", user_id=user_id)

    grand_total = cash

    for pos in posessions:
        symbol = pos["symbol"]
        pos["price"] = lookup(symbol)["price"]
        pos["total"] = pos["price"] * pos["shares"]
        pos["price"] = usd(pos["price"])
        if symbol not in data:
            pos["total"] = usd(pos["total"])
            data[symbol] = pos
        else:
            data[symbol]["shares"] += pos["shares"]
            data[symbol]["total"] += pos["total"]
            data[symbol]["total"] = usd(data[symbol]["total"])

    return render_template("index.html", data=data, cash=usd(cash), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("You did not provide a symbol!")
        elif not request.form.get("shares"):
            return apology("You did not provide a number of shares you would liek to buy!")

        data = {}

        symbol = request.form.get("symbol")
        data["symbol"] = symbol
        shares = request.form.get("shares")

        try:
            int(shares)
        except ValueError:
            return apology("Ivalid input type for shares.")

        shares = int(shares)
        data["shares"] = shares

        if not shares > 0:
            return apology("Number of stock must be a positive integer!")

        res = lookup(symbol)
        if not res:
            return apology("Invalid Ticker Symbol!")

        price = res["price"]

        data["price"] = usd(price)
        data["name"] = res["name"]

        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]
        data["cash"] = usd(cash)

        if cash - shares * price >= 0:
            data["total"] = usd(shares * price)
            data["left"] = usd(cash - shares * price)
            cash -= shares * price
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash, user_id=session["user_id"])
            db.execute("INSERT INTO purchases ( id, symbol, price, shares ) VALUES ( :user_id, :symbol, :price, :shares )",
                       user_id=session["user_id"], symbol=symbol, price=price, shares=shares)
            db.execute("INSERT INTO posessions ( id, symbol, shares ) VALUES ( :user_id, :symbol, :shares )",
                       user_id=session["user_id"], symbol=symbol, shares=shares)
            return render_template("buy-invoice.html", data=data)
        else:
            return apology("You dont have enough cash on your account to buy these stocks!")

    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    if len(username) >= 1:
        usernames = [dct["username"] for dct in db.execute("SELECT username FROM users")]
        if username not in usernames:
            return jsonify(True)
        else:
            return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    purchases = db.execute("SELECT * FROM purchases WHERE id = :user_id", user_id=user_id)
    sales = db.execute("SELECT * FROM sales WHERE id = :user_id", user_id=user_id)
    for pur in purchases:
        pur["type"] = "purchase"
    for sale in sales:
        sale["type"] = "sale"
    transactions = purchases + sales
    transactions.sort(key=lambda tr: tr['date'])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("You did not provide a stock to look up!")

        stock = request.form.get("symbol")

        res = lookup(stock)
        if not res:
            return apology("Invalid Ticker Symbol!")

        price = usd(res['price'])

        if not res:
            return apology("Invalid Symbol!")
        else:
            return render_template("quoted.html", res=res, price=price)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("You must provide a username!")

        elif not request.form.get("password"):
            return apology("You must provide a password!")

        elif not request.form.get("confirmation"):
            return apology("You must type a password again as well!")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Your password don;t match!")

        usernames = [a["username"] for a in db.execute("SELECT username FROM users")]

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        if username in usernames:
            return apology("A user with such username already exists!")
        else:
            db.execute("INSERT INTO users ( username, hash ) VALUES ( :username, :password )",
                       username=username, password=password)

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    data = {}
    user_id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)[0]["cash"]
    posessions = db.execute("SELECT * FROM posessions WHERE id = :user_id", user_id=user_id)

    grand_total = cash

    for pos in posessions:
        symbol = pos["symbol"]
        pos["price"] = lookup(symbol)["price"]
        pos["total"] = pos["price"] * pos["shares"]
        if symbol not in data:
            data[symbol] = pos
        else:
            data[symbol]["shares"] += pos["shares"]
            data[symbol]["total"] += pos["total"]

    if request.method == "POST":
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("You didn't select stock you wanted to sell or number of shares!")

        try:
            int(request.form.get("shares"))
        except ValueError:
            return apology("Incorrect value type of shares number!")

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if data[symbol]["shares"] > shares:
            price = lookup(symbol)["price"]
            cash_earned = shares * price
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash+cash_earned, user_id=user_id)
            new_shares = data[symbol]["shares"] - shares
            db.execute("DELETE FROM posessions WHERE id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)
            db.execute("INSERT INTO posessions ( id, symbol, shares) VALUES ( :user_id, :symbol, :new_shares )",
                       user_id=user_id, symbol=symbol, new_shares=new_shares)
            db.execute("INSERT INTO sales ( id, symbol, price, shares ) VALUES ( :user_id, :symbol, :price, :shares )",
                       user_id=user_id, symbol=symbol, price=price, shares=shares)
            return redirect("/")

        elif data[symbol]["shares"] == shares:
            price = lookup(symbol)["price"]
            cash_earned = shares * price
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash+cash_earned, user_id=user_id)
            db.execute("DELETE FROM posessions WHERE id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)
            db.execute("INSERT INTO sales ( id, symbol, price, shares ) VALUES ( :user_id, :symbol, :price, :shares )",
                       user_id=user_id, symbol=symbol, price=price, shares=shares)
            return redirect("/")
        else:
            return apology("You don't have that much shares of this stock!")

    else:
        symbols = data.keys()
        return render_template("sell.html", symbols=symbols)


@app.route("/donate", methods=["GET", "POST"])
@login_required
def donate():
    """Adds cash to your account."""
    if request.method == "POST":
        donation = request.form.get("donation")
        try:
            float(donation)
        except ValueError:
            return apology("Invalid sum of donation!")
        donation = float(donation)
        if 100 <= donation <= 10000:
            cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]
            cash += donation
            db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash, user_id=session["user_id"])
            return redirect("/")
        else:
            return apology("You can donate only from $100 to $10000")
    else:
        return render_template("donate.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


