import socket, threading
from helpers.itineraries import find_itineraries, get_player_node
from helpers.parser import make_http_response, parse_http_request
from helpers.graphManager import Graph
from helpers.dbManager import recover_landmarks, recover_distances
from heartbeat.heartbeat import join_bootstrap
from helpers.configManager import get, hermes_get
from urllib import parse
import requests
import random
import subprocess

#Cloud ip and port
CLOUD_IP = get("CLOUD_IP")
CLOUD_PORT = int(get("CLOUD_PORT")) 

#ID of the fog node
FOG_ID = int(hermes_get("ID"))

port = int(get("FOG_PORT"))
   
MY_IP = subprocess.check_output("dig +short myip.opendns.com @resolver1.opendns.com", shell=True).decode("utf-8").split("\n")[0]
BOOTSTRAP_IP = get("BOOTSTRAP_IP")
ACCEPT_LIST_PORT = int(get("BOOTSTRAP_PORT"))
BEAT_PORT = int(get("BEAT_PORT"))

print(FOG_ID)
print(MY_IP)
def bootstrap():
    join_bootstrap(25, MY_IP, "1214.234", "1114.243", BOOTSTRAP_IP, ACCEPT_LIST_PORT,
                   BEAT_PORT, 10)


class ClientThread(threading.Thread):

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print("[+] New thread started for "+ip+":"+str(port))

    def run(self):
        print("Connection from : "+ip+":"+str(port))

        #clientsock.send(bytes("Welcome to the server\n", "UTF-8"))
        data = self.csocket.recv(2048)

        decoded = data.decode("UTF-8")

        #extract parameters from http requests
        parameters = parse_http_request(decoded)

        #check if request has all the necessary parameters
        if ("latitude" not in parameters or "longitude" not in parameters or "interval" not in parameters or "trans" not in parameters):
            print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), "Invalid request"))
            response = make_http_response(400)
            self.csocket.send(response.encode("utf-8"))
        else:
            node_index, dist, lat, long = get_player_node(parameters["latitude"] , parameters["longitude"], landmarks, parameters["trans"])
            
            print(node_index, dist, infinite_distances_walking[node_index])
            if int(parameters["interval"]) - dist < 0:
                json_res = "[{}]"

                #trasform into http response
                response = make_http_response(200, parameters["version"], json_res)
                
                print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), parameters))

                #send response
                self.csocket.send(response.encode("utf-8"))
            else:
                if (parameters["trans"] == "0"):
                    check = g_walking.check_index(node_index) and infinite_distances_walking[node_index] > int(parameters["interval"])-dist
                else:
                    check = g_driving.check_index(node_index) and infinite_distances_driving[node_index] > int(parameters["interval"])-dist
                

                if check:
                    #Handle locally
                    print("Handle request locally")

                    #calculate itineraries from parameters
                    if (parameters["trans"] == "0"):
                        json_res = find_itineraries(node_index, int(parameters["interval"]) - dist, g_walking, landmarks, dist, "walking", parameters["latitude"] , parameters["longitude"])
                    else:
                        json_res = find_itineraries(node_index, int(parameters["interval"]) - dist, g_driving, landmarks, dist, "driving", parameters["latitude"] , parameters["longitude"])
                    
                    #trasform into http response
                    response = make_http_response(200, parameters["version"], json_res)
                    
                    print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), parameters))

                    #send response
                    self.csocket.send(response.encode("utf-8"))
                else:
                    #Send to cloud
                    print("Sent request to Cloud")

                    #pop version from parameters
                    version = parameters.pop('version', None)
                    #request the cloud with the original parameters
                    url = "http://" + CLOUD_IP + ":" + str(CLOUD_PORT)
                    parameters["latitude"] = lat
                    parameters["longitude"] = long
                    parameters["interval"] = round(int(parameters["interval"]) - dist)
                    r = requests.get(url, parameters)

                    #send response
                    response = make_http_response(200, version, r.text)                
                    self.csocket.send(response.encode("utf-8"))
                


        print("Client at "+self.ip+" disconnected...")
        self.csocket.close()

#load itineraries from db
print(FOG_ID)
landmarks = recover_landmarks(FOG_ID)

print("Landmarks recovered")

print(len(landmarks))
# Call google maps for distances
distances = recover_distances()

print("Distances recovered")

#create graph for walking
g_walking = Graph(len(landmarks))

only_walking = []   

for i in distances:
    if i["Transport"] == "walking":
        only_walking.append(i)

g_walking.build_graph(landmarks, only_walking)
#random weights for now
g_walking.set_nodes_weights()
g_walking.set_nodes_times()

print("Graph for walking built")

#g_walking.print_agraph()

#create graph for driving
g_driving = Graph(len(landmarks))

only_driving = []   

for i in distances:
    if i["Transport"] == "driving":
        only_driving.append(i)

g_driving.build_graph(landmarks, only_walking)
#random weights for now
g_driving.set_nodes_weights()
g_driving.set_nodes_times()

print("Graph for driving built")

#g_driving.print_agraph()


#get distance from infinite for walking
infinite_distances_walking = g_walking.bellman_ford(-1)

print(infinite_distances_walking)
print("Distance from infinite calculated for walking")

#get distance from infinite for dricing
infinite_distances_driving = g_driving.bellman_ford(-1)

print("Distance from infinite calculated for driving")


t3 = threading.Thread(target=bootstrap)
t3.start()

print("Connected to bootstrap")

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = "0.0.0.0"
tcpsock.bind((host,port))

while True:
    tcpsock.listen(4)
    print("Listening for incoming connections...\n")

    (clientsock, (ip, port)) = tcpsock.accept()

    #pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()

