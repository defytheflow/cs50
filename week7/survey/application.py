import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    print(request.form.get("name"))
    if not request.form.get("name") or not request.form.get("nick") or not request.form.get("assessment"):
        return render_template("error.html", message="You did not provide your name or nickname!")
    with open("survey.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow((request.form.get("name"), request.form.get("nick"),
                         request.form.get("lang"), request.form.get("assessment")))
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", "r") as f:
        reader = csv.reader(f)
        surveys = list(reader)
    return render_template("sheet.html", surveys=surveys)
