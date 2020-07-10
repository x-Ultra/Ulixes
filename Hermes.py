import socket, threading
from helpers.itineraries import find_itineraries
from helpers.parser import make_http_response, parse_http_request
from helpers.graphManager import Graph
from helpers.dbManager import load_from_DB, recover_distances
from urllib import parse
import requests
import random

#Cloud ip and port
CLOUD_IP = "127.0.0.1"
CLOUD_PORT = 5005  

#ID of the fog node
FOG_ID = 1

#DEBUG, 1 to send all requests to cloud
#       0 to handle all requests locally
ASK_CLOUD = 0

host = "0.0.0.0"
port = 8888

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

        data = "dummydata"

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
            #calculate itineraries from parameters
            json_res = find_itineraries((parameters["latitude"] , parameters["longitude"]), parameters["interval"], parameters["trans"])

            if ASK_CLOUD == 0:
                #trasform into http response
                response = make_http_response(200, parameters["version"], json_res)
                
                print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), parameters))

                #send response
                self.csocket.send(response.encode("utf-8"))
            else:
                #pop version from parameters
                version = parameters.pop('version', None)
                
                #request the cloud with the original parameters
                url = "http://" + CLOUD_IP + ":" + str(CLOUD_PORT)
                r = requests.get(url, parameters)

                #send response
                response = make_http_response(200, version, r.text)                
                self.csocket.send(response.encode("utf-8"))
                


        print("Client at "+self.ip+" disconnected...")
        self.csocket.close()

#load itineraries from db
landmarks = load_from_DB("Landmarks", FOG_ID)

print("Landmarks recovered")

# Call google maps for distances
distances = recover_distances(landmarks)

print("Distances recovered")

#create graph
g = Graph(len(landmarks))
g.build_graph(landmarks, distances)
#random weights for now
g.set_nodes_weights()
print("Graph built")

g.print_agraph()

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))

while True:
    tcpsock.listen(4)
    print("Listening for incoming connections...\n")

    (clientsock, (ip, port)) = tcpsock.accept()

    #pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()