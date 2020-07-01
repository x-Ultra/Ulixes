from pwn import *
import threading
import time
import requests

context.log_level = 10000000

NBR_CONNECTIONS = 5
NBR_REQUESTS = 100
BYTES_PER_REQUESTS = 100

class ClientThread(threading.Thread):
	def __init__(self, r, idt):
		threading.Thread.__init__(self)
		self.r = r
		self.idt = idt

	def run(self):
		start = time.time()
		for i in range(NBR_REQUESTS):
			self.r.send("A"*BYTES_PER_REQUESTS)
			#print("[+"+str(self.idt)+"+] Sent " + str(BYTES_PER_REQUESTS) +" bytes")
			recvd = self.r.recv()
			#print("[+"+str(self.idt)+"+] Received " + str(len(recvd)) +" bytes")
		self.r.close()
		print(time.time() - start)

def spammer():
	for i in range(NBR_CONNECTIONS):
		r = remote("127.0.0.1", "5005")
		newthread = ClientThread(r, i)
		newthread.start()

def single_request():
	url = "http://127.0.0.1:5005"
	params = {"latitude": "42", "longitude": "42", "interval": "27", "trans" : "0"}
	r = requests.get(url, params = params)
	print(r.text)

single_request()