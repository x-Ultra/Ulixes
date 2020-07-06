class AdjNode:
    def __init__(self, value, weight):
        self.vertex = value
        self.weight = weight
        self.next = None


class Graph:
	def __init__(self, num):
	    self.V = num
	    self.graph = [None] * self.V
	    self.nodes_weights = [0]*self.V
	    self.nodes_values = [0]*self.V

	# Add edges
	def add_edge(self, s, d, s_name, d_name, e_weight):
	    node = AdjNode(d, e_weight)
	    node.next = self.graph[s]
	    self.graph[s] = node
	    self.nodes_values[s] = s_name

	    node = AdjNode(s, e_weight)
	    node.next = self.graph[d]
	    self.graph[d] = node
	    self.nodes_values[d] = d_name

	# Print the graph
	def print_agraph(self):
	    for i in range(self.V):
	        print("Vertex " + str(self.nodes_values[i]) + " ( " + str(self.nodes_weights[i]) + " ):", end="")
	        temp = self.graph[i]
	        while temp:
	            print(" -{}-> {}".format(temp.weight, self.nodes_values[temp.vertex]), end="")
	            temp = temp.next
	        print(" \n")


	def set_nodes_weights(self, weights):
		#@ weights, list of nodes weights

		for i in range(0, len(weights)):
			self.nodes_weights[i] = weights[i]

	def build_graph(self, nodes, weights):

		#@ nodes, nodes of the graph [lists of dicts]
		#@ weights, weights of the arches of the graph (list of dicts)

		#@ return, graph as an adiacency list

		for edge in weights:
			try:
				start = edge["Start"]
				end = edge["End"]
				self.add_edge(nodes[start][0], nodes[end][0], start, end, edge["Seconds"])
			except:
				#For now not all distances are covered
				pass
	    	






