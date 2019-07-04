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
        super(Link, self).__init__(*args, **kwargs)
        
    def __repr__(self):
        return '<Link: %s>' % self.id

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

    def __init__(self, *args, **kwargs):
        super(Spot, self).__init__(*args, **kwargs)
        
    def __repr__(self):
        return '<Spot: %s>' % self.id

