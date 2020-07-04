import base64
import json

# function that given the name of a monument (the same name used to save te monument into DynamoDB),
# returns its image after a query into the DB
# TODO can we use cache ?
def get_image_by_name(imageName):
    with open(imageName, "rb") as img_file:
        pict = base64.b64encode(img_file.read())
    return pict.decode("ascii")

# TODO function that given an itinerary, extract the sha-xxx of its string json
def find_itineraries(location, interval, trasport):
    # @ location: t-uple containing two floats in string format in the form (latitude, longitude)
    # @ interval: integer in string format representing the amount of time of the visit
    # @ transport: integer in string format representing the means of transport chosen

    # @ return: a json file containg all the avaible itineraries

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
