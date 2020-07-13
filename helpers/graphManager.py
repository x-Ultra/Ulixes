class AdjNode:
    def __init__(self, value, weight):
        self.vertex = value
        self.weight = weight
        self.next = None


class Graph:
	def __init__(self, num):
	    self.V = num
	    self.graph = {}
	    self.nodes_weights = {}
	    self.nodes_values = {}

	# Add edges
	def add_edge(self, s, d, s_name, d_name, e_weight):
	    node = AdjNode(d, e_weight)
	    node.next = self.graph.get(s)
	    self.graph[s] = node
	    self.nodes_values[s] = s_name

	    node = AdjNode(s, e_weight)
	    node.next = self.graph.get(d)
	    self.graph[d] = node
	    self.nodes_values[d] = d_name

	# Print the graph
	def print_agraph(self):
	    for k, i in self.graph.items():
	        print("Vertex " + str(self.nodes_values[k]) + " ( " + str(self.nodes_weights[k]) + " ):", end="")
	        temp = i
	        while temp:
	            print(" -{}-> {}".format(temp.weight, self.nodes_values[temp.vertex]), end="")
	            temp = temp.next
	        print(" \n")

	    #print(self.graph)


	def set_nodes_weights(self, weights=None):
		#@ weights, dict of nodes weights

		if weights == None:
			import random
			
			for k in self.graph:	
				self.nodes_weights[k] = random.randint(0, 100)
		else:
			self.nodes_weights = weights

	def build_graph(self, nodes, weights):

		#@ nodes, nodes of the graph [lists of dicts]
		#@ weights, weights of the arches of the graph (list of dicts)

		#@ return, graph as an adiacency list

		infinito = {}
		for edge in weights:
			#print(edge)
			start = edge["Start"]
			end = edge["End"]
			#print(nodes[start][0], nodes[end][0], start, end, edge["Seconds"])

			#if both in local graph
			if nodes.get(start) != None and nodes.get(end) != None:
				self.add_edge(nodes[start][0], nodes[end][0], start, end, edge["Seconds"])
			#If start is not in local graph
			elif nodes.get(start) == None and nodes.get(end) != None:
				#if this is the closest to end until now
				if infinito.get(nodes[end][0]) == None or int(infinito.get(nodes[end][0])[1]) > int(edge["Seconds"]):
					infinito[nodes[end][0]] = (end, edge["Seconds"])
			#if end is not in local graph
			elif nodes.get(start) == None and nodes.get(end) != None:
				#if this is the closest to start until now
				if infinito.get(nodes[start][0]) == None or int(infinito.get(nodes[start][0])[1]) > int(edge["Seconds"]):
					infinito[nodes[start][0]] = (start, edge["Seconds"])

		for k, v in infinito.items():
			self.add_edge(-1, k, "Infinito", v[0], v[1])

	# Implementation of bellman - Ford algorithm
	def bellman_ford(self, src):  

		#@ src, source index for the algorithm

		#@ return, minimum distances from the source node

		#Inizialize ditances
		dist = {}
		dist[src] = 0
		nodes = list(self.graph.keys())
		for i in nodes:
			if i != src:
				dist[i] = float("inf")

  		#Iterate
		for m in range(self.V - 1):  
			#Calcualate distances
			for u in nodes:
				adj = self.graph[u] 
				while adj:
					if dist[u]!= float("Inf") and dist[u] + int(adj.weight) < dist[adj.vertex]:  
						dist[adj.vertex] = dist[u] + int(adj.weight)
					adj = adj.next  

		# return result 
		return dist  	    	

	# Function to che if and index is part of the graph
	def check_index(self, index):
		return self.graph.get(index) != None



