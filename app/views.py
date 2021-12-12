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

# bring in ev car correlation
corr_final = get_corr(ev_raw)
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

        req = request.form
        zip = req["zip"]
        car_brand_1 = req["car_brand_1"]
        car_1 = req["car_1"]
        car_brand_2 = req["car_brand_2"]
        car_2 = req["car_2"]


        ### Toggle on for testing purposes
        # zip = '78210'
        # car_brand_1 = 'Ford'
        # car_1 = 'Mustang Mach-E SR AWD'
        # car_brand_2 = 'Tesla'
        # car_2 = 'Cybertruck Tri Motor'


        return redirect(url_for('vehicle_selected',zip = zip,car_brand_1 = car_brand_1, car_1 = car_1,
        car_brand_2 = car_brand_2, car_2 = car_2))

    return render_template("public/select_car.html")


@app.route("/vehicle_selected/,<car_brand_1>,<car_1>,<car_brand_2>,<car_2>,<zip>", methods=["GET", "POST"])
def vehicle_selected(car_brand_1,car_1,car_brand_2,car_2,zip):
    zip = zip
    c_table = get_comparison_table(ev_df,car_1,car_2)
    range_1 = get_range(ev_range,car_1)
    range_2 = get_range(ev_range,car_2)

    similar_cars_1 = get_similar(corr_final,car_1)
    similar_cars_2 = get_similar(corr_final,car_2)

    poi = get_poi(zip,us_zip_lat_long_data)
    zoom = get_zoom(range_1,range_2)
    rel_path = "static/iframe_figures"
    r_string = "figure_9.html"
    path = os.path.join(rel_path, r_string)

    map_loc = radius_map(zip,us_zip_lat_long_data,range_1,range_2)

    return render_template("public/vehicle_selected.html",c_table=[c_table.to_html()],
                    similar_cars_1=[similar_cars_1.to_html(index=False)],
                    similar_cars_2=[similar_cars_2.to_html(index=False)],
                    zip = zip,car_brand_1 = car_brand_1, car_1 = car_1,
                    car_brand_2 = car_brand_2, car_2 = car_2,range_1 = range_1, range_2 = range_2,
                    poi = poi, zoom = zoom)


@app.route("/data")
def data():
    ev_df
    return render_template("public/data.html",ev_df=[ev_df.to_html()] )

@app.route("/about")
def about():

    return render_template("public/about.html")
