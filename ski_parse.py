from urllib2 import urlopen
from lxml import etree
import json

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
    return j_pistes


if __name__ == '__main__':
    # get the latest xml file
    j_pistes = get_conditions()
    print(json.dumps(j_pistes, indent=4, sort_keys=True, ensure_ascii=False))
