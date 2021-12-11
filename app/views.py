from app import app
from flask import render_template, request, redirect
import pandas as pd
import numpy as np
import requests, io, json
from flask import url_for
import random

import plotly.express as px
import geopandas as gpd
import shapely.geometry

from ev import *
from radius_map import *

from datetime import datetime





@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

date = datetime.utcnow()

ev_raw,ev_range,ev_df = ev_data()



@app.route("/")
def index():
     return render_template("public/index.html")


@app.route("/select_car", methods=["GET", "POST"])
def select_car():

    if request.method == "POST":

        req = request.form
        zip = req["zip"]
        car_1 = req["car_1"]
        car_2 = req["car_2"]
        return redirect(url_for('vehicle_selected',zip = zip,car_1 = car_1,car_2 = car_2))

    return render_template("public/select_car.html")


@app.route("/vehicle_selected/<car_1>,<car_2>", methods=["POST"])
def vehicle_selected(car_1,car_2):
    c_table = get_comparison_table(ev_df,car_1,car_2)

    return render_template("public/vehicle_selected.html",tables=[c_table.to_html()])


@app.route("/zip")
def zip():
    # Strings
    my_name = "Mark"
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Get distinct Brands
    brands = ev_df['Brand'].unique()

    car_1 = 'Mustang Mach-E SR AWD'
    car_2 = 'ID.4 GTX'
    c_table = get_comparison_table(ev_df,car_1,car_2)

    return render_template("public/zip.html",my_name=my_name, langs=langs,
        ev_range=ev_range, brands=brands, tables=[c_table.to_html()])


@app.route("/about")
def about():
    return render_template("public/about.html")


users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creatof of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}

@app.route("/profile/<username>")
def profile(username):

    user = None

    if username in users:
        user = users[username]

    return render_template("public/profile.html", username=username, user=user)

@app.route("/multiple/<foo>/<bar>/<baz>")
def multiple(foo, bar, baz):

    print(f"foo is {foo}")
    print(f"bar is {bar}")
    print(f"baz is {baz}")


    return f"foo is {foo}, bar is {bar}, baz is {baz}"

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        req = request.form

        username = req["username"]
        email = req["email"]
        password = req["password"]


        return redirect(request.url)

    return render_template("public/sign_up.html")



@app.route("/jinja")
def jinja():

    # Strings
    my_name = "Mark"

    # Integers
    my_age = 30

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description
            self.domain = domain

        def pull(self):
            return f"Pulling repo '{self.name}'"

        def clone(self, repo):
            return f"Cloning into {repo}"

    my_remote = GitRemote(
        name="Learning Flask",
        description="Learn the Flask web framework for Python",
        domain="https://github.com/Julian-Nash/learning-flask.git"
    )

    my_html = "<h1>This is some HTML</h1>"

    suspicious = "<script>alert('NEVER TRUST USER INPUT!')</script>"

    # Functions
    def repeat(x, qty=1):
        return x * qty

    return render_template(
        "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
        friends=friends, colors=colors, cool=cool, GitRemote=GitRemote,
        my_remote=my_remote, repeat=repeat, date=date, my_html=my_html, suspicious=suspicious

    )
