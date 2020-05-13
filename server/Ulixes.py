import socket, threading
from parser import parse_request

host = "0.0.0.0"
port = 5005

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

        while len(data):
            # TODO here extract HTTP parameter
            data = self.csocket.recv(2048)

            decoded = data.decode("UTF-8")

            print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), decoded))

            res = parse_request(decoded)
            print(res)
            sendBack = bytes("You sent me : "+decoded, "UTF-8")

            self.csocket.send(sendBack)

        print("Client at "+self.ip+" disconnected...")

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