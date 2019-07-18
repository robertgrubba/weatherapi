import datetime
import hashlib

from app import db

def sha1(s):
    return hashlib.sha1(s).hexdigest().lower()

class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer)
    ltype = db.Column(db.String(5))
    link = db.Column(db.String(250))

    def __init__(self, *args, **kwargs):
        super(Links, self).__init__(*args, **kwargs)
        
    def __repr__(self):
        return '<Links: %s>' % self.id

class Spots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    windguru_id = db.Column(db.Integer)
    spot_country = db.Column(db.String(250))
    spot_name = db.Column(db.String(250))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    spd_min = db.Column(db.Float)
    spd_max = db.Column(db.Float)
    dir_max = db.Column(db.Integer)
    dir_min = db.Column(db.Integer)
    elev = db.Column(db.SmallInteger)
    type = db.Column(db.SmallInteger)

    def __init__(self, *args, **kwargs):
        super(Spots, self).__init__(*args, **kwargs)
        
    def __repr__(self):
        return '<Spots: %s>' % self.id

class Forecasts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	windguru_id = db.Column(db.Integer)
	tmp = db.Column(db.Float)
	tcdc = db.Column(db.Integer)
	hcdc = db.Column(db.Integer)
	mcdc = db.Column(db.Integer)
	lcdc = db.Column(db.Integer)
	rh = db.Column(db.Integer)
	gust = db.Column(db.Float)
	slp = db.Column(db.Float)
	flhgt = db.Column(db.Integer)
	apcp = db.Column(db.Integer)
	windspd = db.Column(db.Float)
	winddir = db.Column(db.Integer)
	smern = db.Column(db.Integer)
	tmpe = db.Column(db.Float)
	pcpt = db.Column(db.Float)
	hr_weekday = db.Column(db.Integer)
	hr_h = db.Column(db.Integer)
	hr_d = db.Column(db.Integer)
	hours = db.Column(db.Integer)
	flyable = db.Column(db.SmallInteger)
	
	def __init__(self, *args, **kwargs):
        	super(Forecasts, self).__init__(*args, **kwargs)
        
	def __repr__(self):
        	return '<Forecasts: %s>' % self.id

