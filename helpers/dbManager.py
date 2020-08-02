import boto3
from boto3.dynamodb.conditions import Key
from helpers.configManager import get
from helpers.configManager import cred_get

USE_DINAMODB_LAND = get("USE_DINAMODB_LAND") == "True"
USE_DINAMODB_DIST = get("USE_DINAMODB_DIST") == "True"

def get_landmarks(fog_id=None):

	#@ fog_id: int, id of the fog node that colled this function
	#@ return: list of items corressponding to the fog id or all the items

	#Set up boto3
	dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', 
    aws_access_key_id=cred_get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=cred_get("AWS_SECRET_ACCESS_KEY"))
	table = dynamodb.Table("Landmarks")

	print("ciao", fog_id)
	if (fog_id == None):
		print("None")
		# recover all items
		resp = table.scan(ProjectionExpression = '#n, ID, Lat, #l, Description, PictureUrl',
                  ExpressionAttributeNames = {'#n': 'Name', '#l' : 'Long'})
	else:
		print("ciao")
		#Recover items corrisponding to a specific fog_id
		resp = table.scan(ProjectionExpression = '#n, ID, Lat, #l, Description, PictureUrl',
                  ExpressionAttributeNames = {'#n': 'Name', '#l' : 'Long'},
                  ExpressionAttributeValues= {
			        ":FogId": 1,
				  },
                  FilterExpression="Fog"+str(fog_id)+" = :FogId")

	return resp['Items']

def get_distances(fog_id=None):

	#@ fog_id: int, id of the fog node that called this function
	#@ return: list of items corressponding to the fog id or all the items

	#Set up boto3
	dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', 
    aws_access_key_id=cred_get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=cred_get("AWS_SECRET_ACCESS_KEY"))
	table = dynamodb.Table("Distances")

	if (fog_id == None):
		# recover all items
		resp = table.scan(ProjectionExpression = '#s, #e, Seconds, Transport',
                  ExpressionAttributeNames = {'#s': 'Start', '#e' : 'End'})
	else:
		#Recover items corrisponding to a specific fog_id
		resp = table.scan(ProjectionExpression = '#s, #e, Seconds, Transport',
                  ExpressionAttributeNames = {'#s': 'Start', '#e' : 'End'},
                  ExpressionAttributeValues= {
			        ":FogId": 1,
				  },
                  FilterExpression="Fog"+str(fog_id)+" = :FogId")


	return resp['Items']



def readCSV(filename):
	fd = open(filename, "r")

	lines = fd.readlines()

	names = lines[0].strip().split(", ")

	print(names)
	final_list = []
	for i in range(1, len(lines)):
		values = lines[i].strip().split(", ")
		if len(values) != len(names):
			values = lines[i].strip().split(",")
		dict_info = {}	
		for j in range(len(names)):
			dict_info[names[j]] = values[j].strip()
		final_list.append(dict_info)

	return final_list


def recover_landmarks(fog_id=None):

	#@ return: dict of landmarks, the dict is  "Name" =>  ( "ID", "Lat" , "Long", "Url", "Description") 

	res = {}
	if USE_DINAMODB_LAND:
		print("recover", fog_id)
		items = get_landmarks(fog_id)
		print(len(items))
		for item in items:
			#print(item)
			#print(item["Name"])
			res[item["Name"]] = (int(item["ID"]), float(item["Lat"]) , float(item["Long"]), item["PictureUrl"], item["Description"])
	else:
		fd = open("landmarksComplete.csv", "r")

		lines = fd.readlines()
		for i in range(1, len(lines)):
		    splitted = lines[i].strip().split(", ")
		    if (fog_id == None or splitted[fog_id+2] == "1"):
		    	res[splitted[0]] = (i-1, splitted[1], splitted[2], splitted[5], splitted[6])
		fd.close()
	#print(res)
	return res

def recover_distances(fog_id=None):

	#@ landmarks: list of lists of landmarks, the second list is [ "Name", "Lat" , "Long" ]
	#@ return: list of dict with key "Start" "End" "Seconds" and "Transport"

	# too poor to call google every time

	res = []
	if USE_DINAMODB_DIST:
		res = get_distances(fog_id)
	else:
		fd = open("distancesDB.csv", "r")

		lines = fd.readlines()

		for i in range(1, len(lines)):
		    splitted = lines[i].strip().split(", ")
		    if (fog_id == None or splitted[fog_id+3] == "1"):
		    	res.append({"Start": splitted[0], "End": splitted[1], "Seconds": splitted[2], "Transport": splitted[3]})
		fd.close()

	return res


	# fd1 = open("rawResult2.txt", "a")
	# fd2 = open("distance2.csv", "a")


	# API_KEY = "<censored>"

	# transport = "walking"
	# gmaps = googlemaps.Client(key=API_KEY)
	# for i in range(1, len(landmarks)-1):
	#     for j in range(i+1, len(landmarks)):
	#         origin = (landmarks[i][1], landmarks[i][2])
	#         destination = (landmarks[j][1], landmarks[j][2])
	#         result = gmaps.distance_matrix(origin, destination, mode=transport)

	#         print(i, j)
	#         print(result)
	#         fd1.write(str(result) + "\n")
	#         fd2.write(landmarks[i][0] + ", " + landmarks[j][0] + ", " + str(result["rows"][0]["elements"][0]["duration"]["value"]) + ", " + transport + "\n")

	# transport = "driving"
	# for i in range(1, len(landmarks)-1):
	#     for j in range(i+1, len(landmarks)):
	#         origin = (landmarks[i][1], landmarks[i][2])
	#         destination = (landmarks[j][1], landmarks[j][2])
	#         result = gmaps.distance_matrix(origin, destination, mode=transport)

	#         print(i, j)
	#         print(result)
	#         fd1.write(str(result) + "\n")
	#         fd2.write(landmarks[i][0] + ", " + landmarks[j][0] + ", " + str(result["rows"][0]["elements"][0]["duration"]["value"]) + ", " + transport + "\n")

	# fd1.close()
	# fd2.close()