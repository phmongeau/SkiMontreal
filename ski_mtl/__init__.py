# -*- coding: utf-8 -*-
import os
import json
import requests
from datetime import datetime
from flask import Flask, Response, request, url_for, redirect, render_template, flash, abort
from lxml import etree
from werkzeug.contrib.cache import SimpleCache
from werkzeug import secure_filename
from flaskext.sqlalchemy import SQLAlchemy
#from ski_mtl.models import Track

app = Flask(__name__)
app.secret_key = "secrettest"

# Setup DB
if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    user = "testuser"
    pswd = "toto"
    app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgresql+psycopg2://{}:{}@/ski_mtl'.format(user, pswd)

db = SQLAlchemy(app)


class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    data = db.Column(db.String())

    def __init__(self, name=None, data=None):
        self.name = name
        self.data = data

    def __repr__(self):
        return '<Track {}>'.format(self.name)

# Setup Cache
cache = SimpleCache()

# Other configs
ALLOWED_EXTENSIONS = set(['gpx', 'kml'])


@app.route("/add/<place>/<data>")
def test_db(place, data):
    t = Track(place, data)
    db.session.add(t)
    db.session.commit()
    return redirect(url_for('get_map'))


@app.route("/gpx/get/<place>")
def get_gpx(place):
    t = Track.query.filter(Track.name == place).first()
    if t is not None:
        return Response(t.data, mimetype="application/gpx+xml")
    else:
        abort(404)


@app.route("/gpx/list")
def list_gpx():
    return json.dumps([t.name for t in Track.query.all()])


@app.route("/", methods=['GET'])
def get_map():
    return render_template('index.html')


@app.route("/static/index.html")
def get_static_map():
    return redirect(url_for('get_map'))
    #return redirect(url_for('static', filename='index.html'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/contribuer', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        #name = request.form["location"]
        file = request.files['file']
        if file and allowed_file(file.filename):
            placename = secure_filename(file.filename)
            t = Track.query.filter(Track.name == placename).first()
            if t is not None:
                t.data = file.read()
            else:
                t = Track(placename, file.read())

            db.session.add(t)
            db.session.commit()
            flash(u"Le fichier à été téléversé avec succès", "succes");
            return render_template('upload.html')
        else:
            flash(u"Type de fichier invalide", "error");
            return render_template('upload.html'), 415
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route("/conditions.json", methods=['GET'])
def get_conditions():
    # Try to get conditions from the cache
    cond = cache.get('conditions')
    if cond is None:
        cond = dict()

        cond.update(get_ski_conditions())
        cond.update(get_glisse_conditions())

        # Cache conditions for 30 minutes
        if 'ski_error' in cond or 'glisse_error' in cond:
            print "error getting conditions; not caching"
        else:
            cache.set('conditions', cond, timeout=30 * 60)

    return json.dumps(cond, indent=4, sort_keys=True, ensure_ascii=False)


def getXML(url):
    try:
        r = requests.get(url, timeout=3)
        document = r.content
    except requests.exceptions.Timeout:
        print 'ski_timeout'
        return None

    try:
        tree = etree.fromstring(document)
    except etree.XMLSyntaxError:
        print 'ski: parse_error'
        return None

    return tree


def get_ski_conditions():
    url = "http://depot.ville.montreal.qc.ca/conditions-ski/data.xml"

    tree = getXML(url)
    if tree is False:
        return {'ski_error': 'could not parse'}

    pistes = tree.findall('piste')

    j_pistes = {}
    for piste in pistes:
        out = {}
        out["name"] = piste.find('nom').text
        out["open"] = piste.find("ouvert").text
        out["condition"] = piste.find("condition").text
        out["deblaye"] = piste.find("deblaye").text
        out["type"] = "ski"
        arr = piste.find("arrondissement")
        arrondissement = {
                "name": arr.find("nom_arr").text,
                "cle": arr.find("cle").text,
                "date_maj": arr.find("date_maj").text
              }
        out["arrondissement"] = arrondissement
        j_pistes[out["name"]] = out

    with open("ski_mtl/bin/ski_coords.json", "r") as file:
        coords = json.loads(file.read())

    for track in coords:
        lat = track["latitude"]
        lng = track["longitude"]
        if track["name"] in j_pistes:
            j_pistes[track["name"]]["latitude"] = lat
            j_pistes[track["name"]]["longitude"] = lng

    j_pistes["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return j_pistes


def get_glisse_conditions():
    url = "http://depot.ville.montreal.qc.ca/sites-hiver/data.xml"

    tree = getXML(url)
    if tree is False:
        return {'glisse_error': 'could not parse'}

    pistes = tree.findall('glissade')

    j_pistes = {}
    for piste in pistes:
        out = {}
        out["name"] = piste.find('nom').text
        out["open"] = piste.find("ouvert").text
        out["condition"] = piste.find("condition").text
        out["deblaye"] = piste.find("deblaye").text
        out["type"] = "glissade"
        arr = piste.find("arrondissement")
        arrondissement = {
                "name": arr.find("nom_arr").text,
                "cle": arr.find("cle").text,
                "date_maj": arr.find("date_maj").text
              }
        out["arrondissement"] = arrondissement
        j_pistes[out["name"]] = out

    with open("ski_mtl/bin/glisse_coords.json", "r") as file:
        coords = json.loads(file.read())

    for track in coords:
        lat = track["latitude"]
        lng = track["longitude"]
        if track["name"] in j_pistes:
            j_pistes[track["name"]]["latitude"] = lat
            j_pistes[track["name"]]["longitude"] = lng

    j_pistes["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return j_pistes
