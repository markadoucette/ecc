from app import app
from flask import Flask, render_template, request, jsonify, redirect
import pandas as pd
import numpy as np
import requests, io, json
from flask import url_for
import random
from flask_wtf import FlaskForm
from wtforms import SelectField

import plotly.express as px
import geopandas as gpd
import shapely.geometry
import os

from datetime import datetime


from ev import *
from radius_map import *

### Read in data
ev_raw = pd.read_csv('./app/data_files/ev_car_final.csv',index_col=0)

ev_raw,ev_range,ev_df = ev_data(ev_raw)

# US Zip Code and Lat / Long Dataset
us_zip_lat_long_data = pd.read_csv('./app/data_files/us_zip_code_lat_long.csv',
                dtype={'ZIP': str,'LAT': float,'LNG': float})




@app.route("/")
def main():
    carbrands = ev_df['Brand'].unique()
    return render_template('public/index.html', carbrands=carbrands)


@app.route("/carbrand",methods=["POST","GET"])
def carbrand():

    if request.method == 'POST':
        category_id = request.form['category_id']
        print(category_id)
        carmodel = ev_df.index[(ev_df['Brand']== category_id)].unique()
        OutputArray = []
        for carmodel in carmodel:
            outputObj = {
                'id': carmodel,
                'name': carmodel}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)


@app.route("/select_car", methods=["GET", "POST"])
def select_car():

    if request.method == "POST":

        # req = request.form
        # zip = req["zip"]
        # car_brand_1 = req["car_brand_1"]
        # car_1 = req["car_1"]
        # car_brand_2 = req["car_brand_2"]
        # car_2 = req["car_2"]

        zip = '78210'
        car_brand_1 = 'Ford'
        car_1 = 'Mustang Mach-E SR AWD'
        car_brand_2 = 'Tesla'
        car_2 = 'Cybertruck Tri Motor'


        return redirect(url_for('vehicle_selected',zip = zip,car_brand_1 = car_brand_1, car_1 = car_1,
        car_brand_2 = car_brand_2, car_2 = car_2))

    return render_template("public/select_car.html")


@app.route("/vehicle_selected/,<car_brand_1>,<car_1>,<car_brand_2>,<car_2>,<zip>", methods=["GET", "POST"])
def vehicle_selected(car_brand_1,car_1,car_brand_2,car_2,zip):
    zip = zip
    c_table = get_comparison_table(ev_df,car_1,car_2)
    range_1 = get_range(ev_range,car_1)
    range_2 = get_range(ev_range,car_2)

    poi = get_poi(zip,us_zip_lat_long_data)
    zoom = get_zoom(range_1,range_2)
    rel_path = "static/iframe_figures"
    r_string = "figure_9.html"
    path = os.path.join(rel_path, r_string)

    map_loc = radius_map(zip,us_zip_lat_long_data,range_1,range_2)

    return render_template("public/vehicle_selected.html",tables=[c_table.to_html()],
                    zip = zip,car_brand_1 = car_brand_1, car_1 = car_1,
                    car_brand_2 = car_brand_2, car_2 = car_2,range_1 = range_1, range_2 = range_2,
                    poi = poi, zoom = zoom)


# map_loc = map_loc, href=path[4:]




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
