from app import app, db
from flask import jsonify, request, send_file
from models import Spots,Links,Forecasts
import urllib, json, urllib2, os, sys, ssl, hashlib, time,re
from datetime import datetime
from lxml import html
from sqlalchemy import desc
from PIL import Image, ImageDraw, ImageFilter

def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    result = pil_img.copy()
    result.putalpha(mask)
    return result

@app.route('/')
def homepage():
    return 'If you want to use my API, just mail me rgrubba <at> gmail '

@app.route('/isdefined/<string:name>')
def isdefined(name):
	query = db.session.query(Spots).filter_by(spot_name = name).first()
        if query is not None:
            return "&#10037;"
	else:
	    return ""

@app.route('/isflyabletoday/<string:name>')
def isflyabletoday(name):
	query = db.session.query(Spots).filter_by(spot_name = name).first()
	if query is None:
		return ""
	else:
		now = datetime.now()
		today = now.day
		flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>=6).filter(Forecasts.hr_h<=22).first()
		if flyable is None:
			return "&#10008;"
		else:
			return "&#10004;" #flyable

@app.route('/flyabledays/<string:name>')
def flyabledays(name):
	query = db.session.query(Spots).filter_by(spot_name = name).first()
	if query is None:
		return ""
	else:
		now = datetime.now()
		today = now.day
		flyabledays = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter(Forecasts.hr_h>=6).filter(Forecasts.hr_h<=22).group_by(Forecasts.hr_d)
		comment = ""
		if flyabledays is None:
			comment="&#10008;"
		else:
			for flyableday in flyabledays:
				if today <= flyableday.hr_d:
					comment+= str(flyableday.hr_d)+"."+str(now.month)+", "
				else:
					comment+= str(flyableday.hr_d)+"."+str(now.month+1)+", "
			comment = "&#10004; -> "+comment #flyable
	return comment

@app.route('/spot/<string:name>')
def getSpot(name):
    if len(name)<3:
        return jsonify(
                status=400
                )
    numberOfNames = db.session.query(Spots).filter_by(spot_name = name).count()
    if numberOfNames == 1:
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
            lat = query.lat
            lon = query.lon
            windguruID = query.windguru_id
            return jsonify(
                    spotName = spotName,
                    windguruID = windguruID,
                    spdMin = spdMin,
                    spdMax = spdMax,
                    dirMin = dirMin,
                    dirMax = dirMax,
                    lat = lat,
                    lon = lon,
                    links = links,
                    status =200
                    )
    else:
        queries = db.session.query(Spots).filter_by(spot_name = name).all()
        dirMin = []
        dirMax = []
        for query in queries:
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
            dirMin.append(query.dir_min)
            dirMax.append(query.dir_max)
            lat = query.lat
            lon = query.lon
            windguruID = query.windguru_id
        return jsonify(
                spotName = spotName,
                windguruID = windguruID,
                spdMin = spdMin,
                spdMax = spdMax,
                dirMin = dirMin,
                dirMax = dirMax,
                lat = lat,
                lon = lon,
                links = links,
                status =200
                )

@app.route('/windrose/<string:name>')
def drawWindRose(name):
    GoogleMapsAPIKey = os.environ['GOOGLEMAPSAPI']
    if len(name)<3:
        return jsonify(
                status=400
                )
    else:
	    results = db.session.query(Spots).filter_by(spot_name = name)
	    if results is None:
		return jsonify(
			status=404
			)
	    else:
		dirMin = []
		dirMax = []
		for result in results:
			dirMin.append(result.dir_min)
			dirMax.append(result.dir_max)
			lat = result.lat
			lon = result.lon
		googleimg = urllib.urlopen("https://maps.googleapis.com/maps/api/staticmap?center="+str(lat)+","+str(lon)+"&maptype=satellite&scale=2&zoom=15&size=150x150&key="+GoogleMapsAPIKey)
		img = Image.open(googleimg).convert('RGBA')
		windrose = Image.new('RGBA',(300,300),(255,255,255,0))
		draw = ImageDraw.Draw(windrose)
		numberOfResults = results.count()
		for size in range(0,140):
			for x in range(numberOfResults):
				draw.arc([30+size,30+size,270-size,270-size],dirMin[x],dirMax[x],fill=(0,255,0,90))
		composite = Image.alpha_composite(mask_circle_transparent(img,4,16), windrose.rotate(90))
		composite.save("app/"+str(name).lower().replace(" ","")+".png", "PNG")
		return send_file(str(name).lower().replace(" ","")+".png", mimetype='image/png')
