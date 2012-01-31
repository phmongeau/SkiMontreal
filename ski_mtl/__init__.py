import os
import json
import requests
from datetime import datetime
from flask import Flask, request, url_for, redirect, send_from_directory, render_template
from lxml import etree
from werkzeug.contrib.cache import SimpleCache
from werkzeug import secure_filename

app = Flask(__name__)

cache = SimpleCache()

ALLOWED_EXTENSIONS = set(['gpx', 'kml'])
app.config['UPLOAD_FOLDER'] = 'static/gps/'


@app.route("/", methods=['GET'])
def get_map():
    return render_template('index.html')

@app.route("/static/index.html")
def get_static_map():
    return redirect(url_for('get_map'))
    #return redirect(url_for('static', filename='index.html'))



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print "received file"
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print 'accepted', filename
            print(file.read())
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'ok'
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route("/conditions.json", methods=['GET'])
def get_conditions():
    # Try to get conditions from the cache
    cond = cache.get('conditions')
    if cond is None:
        print "not in cache, getting latest conditions"
        cond = dict()

        cond.update(get_ski_conditions())
        cond.update(get_glisse_conditions())

        # Cache conditions for 30 minutes
        if 'ski_error' in cond or 'glisse_error' in cond:
            print "error getting conditions; not caching"
        else:
            cache.set('conditions', cond, timeout=30 * 60)
    else:
        print "using cache"

    return json.dumps(cond, indent=4, sort_keys=True, ensure_ascii=False)


def getXML(url):
    try:
        r = requests.get(url, timeout=3)
        document = r.content
    except requests.exceptions.Timeout:
        print 'ski_timeout'
        return False

    try:
        tree = etree.fromstring(document)
    except etree.XMLSyntaxError:
        print 'ski: parse_error'
        return False

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


#if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port, debug=True)
