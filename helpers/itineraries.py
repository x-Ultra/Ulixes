import base64
import json
from math import radians, cos, sin, asin, sqrt
import googlemaps

USE_GOOGLE = False

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
#Function that recovers the node that is closest to the tourist position
def get_player_node(lat, long, landmarks, transport):

    #@ lat, long: int, int, the postition of the users
    #@ landmarks: list of monuments with coordinates

    #@ return: index of the node closest to the user

    #Read API key from conf
    with open('API_KEY.conf') as json_file:
        data = json.load(json_file)
        API_KEY = data["Google API"]

    # Find 5 closest according to geographic position
    closest = []
    for k, ld in landmarks.items():
        closest = ordered_insert(closest, (ld[0], haversine(lat, long, ld[1], ld[2]), ld[1], ld[2]))[:5]

    if closest[0][1] == 0:
        return closest[0][0], 0, closest[0][2], closest[0][3]

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
    else:
        return closest[0][0], 0, closest[0][2], closest[0][3]


# function that given the name of a monument (the same name used to save te monument into DynamoDB),
# returns its image after a query into the DB
# TODO can we use cache ?
def get_image_by_name(imageName):
    with open("images/" + imageName, "rb") as img_file:
        pict = base64.b64encode(img_file.read())
    return pict.decode("ascii")

# TODO function that given an itinerary, extract the sha-xxx of its string json
def find_itineraries(location, interval, graph):
    # @ location: integer rapresenting the starting node
    # @ interval: integer representing the amount of time of the visit
    # @ graph: the graph

    # @ return: a json file containg all the avaible itineraries

    #print(graph.find_best_path(location, interval))
    
    # pass parameters to algorithm
    colosseoPict = get_image_by_name("colosseo.jpeg")
    piazzaSpagnaPict = get_image_by_name("piazzaSpagna.jpg")
    piramidePict = get_image_by_name("piramide.jpg")

    result = [
        {
            "ID": "coolhash1",
            "MeansOfTransp": "bici",
            "Departure": "9:45",
            "ItineraryMonuments": [
                {
                    "Monument":
                        {
                            "Name": "Colosseo",
                            "Picture": colosseoPict,
                            "Coordinates": "lat1, lon1"
                        },
                    "Position": "1",
                    "ExpectedArrTime": "10:00"
                },
                {
                    "Monument":
                        {
                            "Name": "Piazza Di Spagna",
                            "Picture": piazzaSpagnaPict,
                            "Coordinates": "lat2, lon2"
                        },
                    "Position": "2",
                    "ExpectedArrTime": "12:00"
                },
                {
                    "Monument":
                        {
                            "Name": "Piramide",
                            "Picture": piramidePict,
                            "Coordinates": "lat3, lon3"
                        },
                    "Position": "3",
                    "ExpectedArrTime": "16:00"
                }
            ]
        },
        {
            "ID": "coolhash2",
            "MeansOfTransp": "bici",
            "Departure": "12:45",
            "ItineraryMonuments": [
                {
                    "Monument":
                        {
                            "Name": "Gelateria",
                            "Picture": "",
                            "Coordinates": "lat1, lon1"
                        },
                    "Position": "1",
                    "ExpectedArrTime": "13:00"
                },
                {
                    "Monument":
                        {
                            "Name": "CampusX",
                            "Picture": "",
                            "Coordinates": "lat2, lon2"
                        },
                    "Position": "2",
                    "ExpectedArrTime": "20:00"
                },
                {
                    "Monument": {
                        "Name": "Mensa",
                        "Picture": "",
                        "Coordinates": "lat3, lon3"
                    },
                    "Position": "3",
                    "ExpectedArrTime": "20:30"
                }
            ]
        }
    ]
    return json.dumps(result)
