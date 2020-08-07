import base64
import json
from math import radians, cos, sin, asin, sqrt
import googlemaps
from images import pictureManager
import datetime
from helpers.configManager import get
import pytz
from time import ctime

USE_GOOGLE = get("USE_GOOGLE") == "True"

# formula used to calculate the distance in km between 2 points
# in the globe, given their latitude and longitude
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers.
    return c * r


def ordered_insert(lista, item):
    if len(lista) == 0:
        return [item]

    i = 0
    while i < len(lista) and lista[i][1] < item[1]:
        i += 1

    return lista[:i] + [item] + lista[i:]


# Function that recovers the node that is closest to the tourist position
def get_player_node(lat, long, landmarks, transport):
    # @ lat, long: int, int, the postition of the users
    # @ landmarks: list of monuments with coordinates

    # @ return: index of the node closest to the user

    # Read API key from conf
    with open('API_KEY.conf') as json_file:
        data = json.load(json_file)
        API_KEY = data["Google API"]

    # Find 5 closest according to geographic position
    closest = []
    for k, ld in landmarks.items():
        closest = ordered_insert(closest, (ld[0], haversine(lat, long, ld[1], ld[2]), ld[1], ld[2]))[:5]

    # If we we find a node at distance 0 its the closest use it
    if closest[0][1] == 0:
        return closest[0][0], 0, closest[0][2], closest[0][3]

    # If we can, use google api
    if USE_GOOGLE:
        print("Called Google")
        # Find closest according to google
        if transport == "0":
            transport = "walking"
        else:
            transport = "driving"

        gmaps = googlemaps.Client(key=API_KEY)

        min_dist = 10000000000000
        res = 0

        for i in range(0, len(closest)):
            origin = (lat, long)
            destination = (closest[i][2], closest[i][3])
            result = gmaps.distance_matrix(origin, destination, mode=transport)
            if result["rows"][0]["elements"][0]["duration"]["value"] < min_dist:
                res = i
                min_dist = result["rows"][0]["elements"][0]["duration"]["value"]

        return closest[i][0], min_dist, closest[i][2], closest[i][3]
    # if we cant estimate time with distance
    else:
        if transport == "0":
            return closest[0][0], closest[0][1]*60*60/5, closest[0][2], closest[0][3]
        else:
            return closest[0][0], closest[0][1]*60*60/50, closest[0][2], closest[0][3]
            

# function that given the name of a monument (the same name used to save te monument into DynamoDB),
# returns its image after a query into the DB
# TODO remove after deploy
def get_image_by_name(imageName):
    with open("images/" + imageName, "rb") as img_file:
        pict = base64.b64encode(img_file.read())
    return pict.decode("ascii")

#Function that recovers the name of the monument with his id
def get_monument_name_byID(monumentIndex):
    monumentIndex = int(monumentIndex)
    for k, v in landmarks_info.items():
        if v[0] == monumentIndex:
            return k

def build_json_itineraries(solutions, transp,userLat, userLon, t, graph, dist):
    # @ solutions: list of tuples containing an integer and a list of integers (the node indexes)
    #               [(12, [1,2,3,4]), (1, [1,2])]

    itineraryList = []
    rome = pytz.timezone('Europe/Rome')
    nowNow = datetime.datetime.now(rome)

    count = 0
    for solution in solutions:
        # current time hh:mmù
        now = nowNow
        departure = datetime.datetime.now(rome).strftime('%H:%M')
        itinerary = solution[1]
        # something like [1, 2, 3, 4]
        # array of dictionaries
        monuments = []
        for monumentIndex in itinerary:
            monument = {}
            monName = get_monument_name_byID(monumentIndex)
            monument["Name"] = monName
            monumentImageUrl = landmarks_info[monName][3]
            image = pictureManager.Image(monName, monumentImageUrl)
            try:    
                monument["Picture"] = pictureManager.getBase64Picture(image)
            except:
                monument["Picture"] = ""
            monument["Coordinates"] = str(landmarks_info[monName][1]) + ", " + str(landmarks_info[monName][2])
            monument["Description"] = landmarks_info[monName][4]
            monuments.append(monument)


        itineraryMonuments = []
        position = 1
        for monument in monuments:
            itinMonument = {}
            itinMonument["Monument"] = monument
            itinMonument["Position"] = str(position)

            if position != 1:
                id1 = itinerary[position - 2]
                id2 = itinerary[position - 1]
                secondsToNext = graph.get_distance(id1, id2) + graph.get_visit_time(id1)
                arrTime = now + datetime.timedelta(seconds=secondsToNext)
                itinMonument["ExpectedArrTime"] = arrTime.strftime('%H:%M')
            else:
                id1 = itinerary[position - 1]
                sec = int(dist)
                arrTime = now + datetime.timedelta(seconds=sec)
                itinMonument["ExpectedArrTime"] = arrTime.strftime('%H:%M')

            now = arrTime
            itineraryMonuments.append(itinMonument)
            position = position + 1

        itinerary = {}
        itinerary["MeansOfTransp"] = transp
        itinerary["Departure"] = departure
        itinerary["ItineraryMonuments"] = itineraryMonuments
        itinerary["ID"] = str(userLat) + str(userLon) + transp + str(t) + str(count)
        count = count + 1

        itineraryList.append(itinerary)

    return json.dumps(itineraryList)


def find_itineraries(location, interval, graph, landmarks, dist, transp, lat, lon):
    # @ location: integer rapresenting the starting node
    # @ interval: integer representing the amount of time of the visit
    # @ graph: the graph

    # @ return: a json file containg all the avaible itineraries

    global landmarks_info 
    landmarks_info = landmarks

    solutions = graph.find_best_path(location, interval)
    
    return build_json_itineraries(solutions, transp,lat, lon, interval, graph, dist)

"""
if __name__ == "__main__":
    j = build_json_itineraries([(1, [1, 2, 3]), (2, [2, 3])], "bici", "1234.5", "1233.2", 1000)
    print(j)
"""
