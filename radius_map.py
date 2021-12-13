import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests, io, json
import random
import plotly.express as px
import geopandas as gpd
import shapely.geometry
import plotly.io as pio
import os


## Get Center point Data
def get_poi(zip,us_zip_lat_long_data):
    zip,lat,lng = us_zip_lat_long_data.loc[us_zip_lat_long_data['ZIP']== zip].values[0]

    poi = {"Latitude": lat, "Longitude": lng}
    return poi

## Get zoom for map
def get_zoom(distiance_1,distiance_2):
    if max(distiance_1,distiance_2) >730:
        return 3.25
    elif max(distiance_1,distiance_2) >620:
        return 3.5
    elif max(distiance_1,distiance_2) >540:
        return 3.75
    elif max(distiance_1,distiance_2) >460:
        return 4
    elif max(distiance_1,distiance_2) >380:
        return 4.25
    elif max(distiance_1,distiance_2) >320:
        return 4.5
    elif max(distiance_1,distiance_2) >265:
        return 4.75
    elif max(distiance_1,distiance_2) >225:
        return 5
    elif max(distiance_1,distiance_2) >190:
        return 5.25
    elif max(distiance_1,distiance_2) >160:
        return 5.5
    elif max(distiance_1,distiance_2) >135:
        return 5.75
    elif max(distiance_1,distiance_2) >115:
        return 6
    elif max(distiance_1,distiance_2) >100:
        return 6.25
    else:
        return 6.5


# - Rob Raymond
# - Aug 29th 2021
# - Draw a polygon around point in scattermapbox using python
# - Type Python
# - Availability https://stackoverflow.com/questions/68946831/draw-a-polygon-around-point-in-scattermapbox-using-python

def poi_poly(
    df,
    radius=10 ** 5,
    poi={"Longitude": 29.395776, "Latitude": -98.464401},
    lon_col="Longitude",
    lat_col="Latitude",
    include_radius_poly=False,
):

    # generate a geopandas data frame of the POI
    gdfpoi = gpd.GeoDataFrame(
        geometry=[shapely.geometry.Point(poi["Longitude"], poi["Latitude"])],
        crs="EPSG:4326",
    )
    # extend point to radius defined (a polygon).  Use UTM so that distances work, then back to WSG84
    gdfpoi = (
        gdfpoi.to_crs(gdfpoi.estimate_utm_crs())
        .geometry.buffer(radius)
        .to_crs("EPSG:4326")
    )

    # create a geopandas data frame of all the points / markers
    if not df is None:
        gdf = gpd.GeoDataFrame(
            geometry=df.loc[:, ["Longitude", "Latitude"]]
            .dropna()
            .apply(
                lambda r: shapely.geometry.Point(r["Longitude"], r["Latitude"]), axis=1
            )
            .values,
            crs="EPSG:4326",
        )
    else:
        gdf = gpd.GeoDataFrame(geometry=gdfpoi)

    # create a polygon around the edges of the markers that are within POI polygon
    return pd.concat(
        [
            gpd.GeoDataFrame(
                geometry=[
                    gpd.sjoin(
                        gdf, gpd.GeoDataFrame(geometry=gdfpoi), how="inner"
                    ).unary_union.convex_hull
                ]
            ),
            gpd.GeoDataFrame(geometry=gdfpoi if include_radius_poly else None),
        ]
    )


## Create Radius Map
def radius_map(zip,us_zip_lat_long_data,range_1,range_2):
    poi = get_poi(zip,us_zip_lat_long_data)
    fig = go.Figure(go.Scattermapbox()).update_layout(
        mapbox={
    #         "style": "carto-positron" ,
            "style": "open-street-map",

            "zoom": get_zoom(range_1,range_2),
            "center": {"lat": poi["Latitude"], "lon": poi["Longitude"]},
            "layers": [
                {
                    "source": json.loads(poi_poly(None, poi=poi, radius=1609.34 * range_1).to_json()),
                    "below": "traces",
                    "type": "line",
                    "color": "teal",
                    "line": {"width": 1.5},
                },
                {
                    "source": json.loads(poi_poly(None, poi=poi, radius=1609.34 * range_2).to_json()),
                    "below": "traces",
                    "type": "line",
                    "color": "coral",
                    "line": {"width": 1.5},
                }
            ],

        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    # fig.show()
    # pio.show(fig, renderer='iframe')
    fig.write_html("./app/static/iframe_figures/map_radius.html")
