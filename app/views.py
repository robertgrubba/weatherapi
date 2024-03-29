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
	    return "",404

@app.route('/isflyabletoday/<string:name>')
def isflyabletoday(name):
	query = db.session.query(Spots).filter_by(spot_name = name).first()
	if query is None:
		return "",404
	else:
		now = datetime.now()
		today = now.day
		currenthour = now.hour
		flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>currenthour).filter(Forecasts.hr_h>=6).filter(Forecasts.hr_h<=22).first()
		if flyable is None:
			return "&#10008;"
		else:
			spot = db.session.query(Spots).filter_by(spot_name = name).first()
			spdMax = spot.spd_max
			spdMin = spot.spd_min
			if spot.type!=1:
				flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>currenthour).filter(Forecasts.hr_h>=6).filter(Forecasts.hr_h<=22).filter(Forecasts.windspd<=spdMax).filter(Forecasts.windspd>=spdMin).first()
			else:
				flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>currenthour).filter(Forecasts.hr_h>=10).filter(Forecasts.hr_h<=18).filter(Forecasts.windspd<=spdMax).filter(Forecasts.windspd>=spdMin).filter(Forecasts.lcdc<30).filter(Forecasts.hcdc<30).filter(Forecasts.mcdc<30).filter(Forecasts.tcdc<30).first()
	
			if flyable is not None:
				return "&#10004;" #flyable
			else:
				return "&#10004; / &#10008;" #somewhat flyable
@app.route('/forecastforfivedays/<string:name>')
def forecastforfivedays(name):
	response = ""
	for day in range(6):
		response=response+"<td>"+isflyabletodayv2(name,day+1)+"</td>"
	return response

@app.route('/isflyabletoday/<int:future>/<string:name>')
def isflyabletodayv2(name,future):
	query = db.session.query(Spots).filter_by(spot_name = name).first()
	if query is None:
		return "",404
	else:
		now = datetime.now()
		today = (now.day + future) - 1
		if today>31:
			n = today - 31
			today = n
		currenthour = now.hour
		if future==1:
			flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>currenthour).filter(Forecasts.hr_h>=6).filter(Forecasts.hr_h<=22).first()
			if flyable is None:
				return "&#9730;"
			else:
				spot = db.session.query(Spots).filter_by(spot_name = name).first()
				spdMax = spot.spd_max
				spdMin = spot.spd_min
				if spot.type!=1:
					flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>currenthour).filter(Forecasts.hr_h>=6).filter(Forecasts.hr_h<=22).filter(Forecasts.windspd<=spdMax).filter(Forecasts.windspd>=spdMin).first()
				else:
					flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>currenthour).filter(Forecasts.hr_h>=10).filter(Forecasts.hr_h<=18).filter(Forecasts.windspd<=spdMax).filter(Forecasts.windspd>=spdMin).filter(Forecasts.lcdc<30).filter(Forecasts.hcdc<30).filter(Forecasts.mcdc<30).filter(Forecasts.tcdc<30).first()
				if flyable is not None:
					return "&#9728;" #high chances to be flyable 
				else:
					return "&#9729;" #low chances to be flyable
		else:
			flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>=6).filter(Forecasts.hr_h<=22).first()
			if flyable is None:
				return "&#9730;"
			else:
				spot = db.session.query(Spots).filter_by(spot_name = name).first()
				spdMax = spot.spd_max
				spdMin = spot.spd_min
				if spot.type!=1:
					flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>=6).filter(Forecasts.hr_h<=22).filter(Forecasts.windspd<=spdMax).filter(Forecasts.windspd>=spdMin).first()
				else:
					flyable = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter_by(hr_d=today).filter(Forecasts.hr_h>=10).filter(Forecasts.hr_h<=18).filter(Forecasts.windspd<=spdMax).filter(Forecasts.windspd>=spdMin).filter(Forecasts.lcdc<30).filter(Forecasts.hcdc<30).filter(Forecasts.mcdc<30).filter(Forecasts.tcdc<30).first()
				if flyable is not None:
					return "&#9728;" #high chances to be flyable 
				else:
					return "&#9729;" #low chances to be flyable

@app.route('/flyabledays/<string:name>')
def flyabledays(name):
	query = db.session.query(Spots).filter_by(spot_name = name).first()
	if query is None:
		return "&#10008;"
	else:
		now = datetime.now()
		today = now.day
		flyabledays = db.session.query(Forecasts).filter_by(windguru_id=query.windguru_id).filter_by(flyable=1).filter(Forecasts.hr_h>=6).filter(Forecasts.hr_h<=22).group_by(Forecasts.hr_d)
		comment = ""
		if flyabledays is None:
			comment="&#10008;"
		else:
			for flyableday in flyabledays:
				if today <= (flyableday.hr_d+5):
					comment+= str(flyableday.hr_d)+"/"+str(now.month)+"/"+str(now.year)+", "
				else:
					comment+= str(flyableday.hr_d)+"/"+str(now.month+1)+"/"+str(now.year)+", "
	if len(comment) < 3:
		comment="&#10008;"
	return comment.rstrip(', ')

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
                    ),404
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

@app.route('/forecastlinks/<string:name>')
def forecastLinks(name):
    if len(name)<3:
        return jsonify(
                status=400
                )
    query = db.session.query(Spots).filter_by(spot_name = name).first()
    if query is None:
         return jsonify(
                 status=404
                ),404
    else:
         lat = query.lat
         lon = query.lon
         windguruID = query.windguru_id
         return "<a href='https://www.windguru.cz/"+str(windguruID)+"' target='_blank'>Windguru</a> <a href='https://www.windy.com/"+str(lat)+"/"+str(lon)+"' target='_blank'>Windy</a>"

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
			),404
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
