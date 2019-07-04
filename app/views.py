from app import app, db
from flask import jsonify, request
from models import Spots,Links
import urllib, json, urllib2, os, sys, ssl, hashlib, time,re
from datetime import datetime
from lxml import html
from sqlalchemy import desc

@app.route('/')
def homepage():
    return 'If you want to use my API, just mail me rgrubba <at> gmail '

@app.route('/spot/<string:name>')
def getSpot(name):
    if len(name)<3:
        return jsonify(
                status=400
                )
    else:
        query = db.session.query(Spots).filter_by(spot_name = name).first()
        if query is None:
            return jsonify(
                    status=404
                    )
        else:
            hasLinks = db.session.query(Links).filter_by(spot_id = query.id)
            if hasLinks is None:
                links = "No Links for the spot"
            else:
                links = []
                for item in hasLinks:
                    links.append(item.link)



            spotName = query.spot_name
            spdMin = query.spd_min
            spdMax = query.spd_max
            dirMin = query.dir_min
            dirMax = query.dir_max
            windguruID = query.windguru_id
            return jsonify(
                    spotName = spotName,
                    windguruID = windguruID,
                    spdMin = spdMin,
                    spdMax = spdMax,
                    dirMin = dirMin,
                    dirMax = dirMax,
                    links = links
                    )

