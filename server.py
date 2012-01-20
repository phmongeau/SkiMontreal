import os
import json
from flask import Flask, url_for, redirect
from datetime import datetime
from urllib2 import urlopen
from lxml import etree

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_map():
    return redirect(url_for('static', filename='index.html'))

@app.route("/conditions.json", methods=['GET'])
def get_conditions():
    return get_conditions()


def get_conditions():
    url = "http://depot.ville.montreal.qc.ca/conditions-ski/data.xml"
    document = urlopen(url).read()

    tree = etree.parse(url)
    root = tree.getroot()
    pistes = root.findall('piste')

    j_pistes = {}
    for piste in pistes:
        out = {}
        out["name"] = piste.find('nom').text
        out["open"] = piste.find("ouvert").text
        out["condition"] = piste.find("condition").text
        out["deblaye"] = piste.find("deblaye").text
        arr = piste.find("arrondissement")
        arrondissement = {
                "name": arr.find("nom_arr").text,
                "cle": arr.find("cle").text,
                "date_maj": arr.find("date_maj").text
              }
        out["arrondissement"] = arrondissement
        j_pistes[out["name"]] = out

    with open("bin/ski_coords.json", "r") as file:
        coords = json.loads(file.read())

    for track in coords:
        lat = track["latitude"]
        lng = track["longitude"]
        j_pistes[track["name"]]["latitude"] = lat
        j_pistes[track["name"]]["longitude"] = lng

    #return j_pistes
    j_pistes["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return json.dumps(j_pistes, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
