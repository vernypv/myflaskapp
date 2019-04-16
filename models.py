from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import urllib.parse
import geocoder
import json
import urllib.request

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    # p = Place()  # places = p.query("1600 Amphitheater Parkway Mountain View CA")


class Place(object):
    @staticmethod
    def meters_to_walking_time(meters):
        # 80 meters is one minute walking time
        return int(meters / 80)

    @staticmethod
    def wiki_path(slug):
        return urllib.request.urlopen("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

    @staticmethod
    def address_to_latlng(address):
        g = geocoder.google(address)
        return g.lat, g.lng

    def query(self, address):
        lat, lng = self.address_to_latlng(address)

        query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=10000&gscoord=37.786971%7C-122.399677&format=json'.format(
            lat, lng)

        data = urllib.parse.urlencode(dict).encode("utf-8")
        dict(query_url)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, data=data) as f:
            resp = f.read()
            print(resp)

        g = urllib.request.urlopen(query_url)
        results = g.read()
        g.close()

        data = json.loads(results)

        places = []

        for place in data['query']['geosearch']:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lon']

            wiki_url = self.wiki_path(name)
            walking_time = self.meters_to_walking_time(meters)

            d = {'name': name, 'url': wiki_url, 'time': walking_time, 'lat': lat, 'lng': lng

                 }

            places.append(d)

        return places
