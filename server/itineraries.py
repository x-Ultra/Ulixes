import json

def find_itineraries(location, interval, trasport):

	#@ location: t-uple containing two floats in string format in the form (latitude, longitude)
	#@ interval: integer in string format representing the amount of time of the visit
	#@ transport: integer in string format representing the means of transport chosen

	#@ return: a json file containg all the avaible itineraries

	#pass parameters to algorithm

	result = [
			  {
			    "Departure": "9:45",
			    "ItineraryMonuments": [
			      {
			        "Monument":
			        {
			          "Name": "Colosseo",
			          "Picture": [],
			          "Coordinates": "lat1, lon1"
			        },
			        "Position": "1",
			        "ExpectedArrTime": "10:00"
			      },
			      {
			        "Monument":
			        {
			          "Name": "Piazza Di Spagna",
			          "Picture": [],
			          "Coordinates": "lat2, lon2"
			        },
			        "Position": "2",
			        "ExpectedArrTime": "12:00"
			      },
			      {
			        "Monument":
			        {
			          "Name": "Piramide",
			          "Picture": [],
			          "Coordinates": "lat3, lon3"
			        },
			        "Position": "3",
			        "ExpectedArrTime": "16:00"
			      }
			    ]
			  },
			  {
			    "Departure": "12:45",
			    "ItineraryMonuments": [
			      {
			        "Monument":
			        {
			          "Name": "Gelateria",
			          "Picture": [],
			          "Coordinates": "lat1, lon1"
			        },
			        "Position": "1",
			        "ExpectedArrTime": "13:00"
			      },
			      {
			        "Monument":
			        {
			          "Name": "CampusX",
			          "Picture": [],
			          "Coordinates": "lat2, lon2"
			        },
			        "Position": "2",
			        "ExpectedArrTime": "20:00"
			      },
			      {
			        "Monument": {
			          "Name": "Mensa",
			          "Picture": [],
			          "Coordinates": "lat3, lon3"
			        },
			        "Position": "3",
			        "ExpectedArrTime": "20:30"
			      }
			    ]
			  }
			]

	return json.dumps(result)

