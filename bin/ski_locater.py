# -*- coding: utf-8 -*-
import json
import codecs
import time
from urllib import urlopen
from ski_parse import get_conditions

url = u"http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=false"

def format_spaces(input):
    return input.replace(" ", "+")

def get_coords(place):
    place = format_spaces(place)
    request = url.format(place)
    response = urlopen(request.encode("utf8"))
    j = json.loads(response.read())
    try:
        coords = j["results"][0]["geometry"]["location"]
    except:
        print j
    return coords["lat"], coords["lng"]

if __name__ == '__main__':

    with open("bin/ski_locations.txt") as f:
        file = codecs.getreader("utf-8")(f).read()
        addresses = json.loads(file)

    #locations = get_conditions()

    locations = {}
    for track in addresses:
        name, address = track.values()
        lat, lng = get_coords(address)

        #locations[name]["latitude"] = lat
        #locations[name]["longitude"] = lng
        track["latitude"] = lat
        track["longitude"] = lng

    with open("ski_coords.json", "w") as file:
        out =  json.dumps(addresses, indent=4, sort_keys=True, ensure_ascii=False)
        file.write(out.encode("utf8"))
