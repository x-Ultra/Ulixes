import socket, threading
from helpers.itineraries import find_itineraries, get_player_node
from helpers.parser import make_http_response, parse_http_request
from helpers.graphManager import Graph
from helpers.dbManager import recover_landmarks, recover_distances
from helpers.configManager import get
import googlemaps
from urllib import parse
import random

port = int(get("CLOUD_PORT"))

class ClientThread(threading.Thread):

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print("[+] New thread started for "+ip+":"+str(port))

    def run(self):
        print("Connection from : "+ip)

        #clientsock.send(bytes("Welcome to the server\n", "UTF-8"))

        data = self.csocket.recv(2048)

        decoded = data.decode("UTF-8")

        #extract parameters from http requests
        parameters = parse_http_request(decoded)

        #check if request has all the necessary parameters
        if ("latitude" not in parameters or "longitude" not in parameters or "interval" not in parameters or "trans" not in parameters):
            #print(data)
            print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), "Invalid request"))
            response = make_http_response(400)
            self.csocket.send(response.encode("utf-8"))
        else:
            if int(parameters["interval"]) < 0:
                json_res = "[{}]"
            else:
                node_index, dist, lat, long = get_player_node(parameters["latitude"] , parameters["longitude"], landmarks, parameters["trans"])

                if int(parameters["interval"]) - dist < 0:
                    json_res = "[{}]"
                else:
                    #calculate itineraries from parameters
                    if (parameters["trans"] == "0"):
                        json_res = find_itineraries(node_index, int(parameters["interval"]) - dist, g_walking, landmarks, dist, "walking", parameters["latitude"] , parameters["longitude"])
                    else:
                        json_res = find_itineraries(node_index, int(parameters["interval"]) - dist, g_driving, landmarks, dist, "driving", parameters["latitude"] , parameters["longitude"])
                    
            #trsform into http response
            response = make_http_response(200, parameters["version"], json_res)
            
            print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), parameters))

            #send response
            self.csocket.send(response.encode("utf-8"))

        print("Client at "+self.ip+" disconnected...")
        self.csocket.close()

#load itineraries from db
landmarks = recover_landmarks()

print("Landmarks recovered")

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

# [{"Start": "noem di start" , "End" : "nome"}, {}]
for i in distances:
    if i["Transport"] == "driving":
        only_driving.append(i)

g_driving.build_graph(landmarks, only_driving)
#random weights for now
g_driving.set_nodes_weights()
g_driving.set_nodes_times()
print("Graph for driving built")

#g_driving.print_agraph()

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