import snap
import math
import random

class UNGraph(object):
	""" Undirected Graph class """

	# Use snap's TUNGraph - We won't have to add each edge twice.
	graph = snap.TUNGraph.New()

	def __init__(self, nodes=[], edges=[]):
		self.nodes = nodes
		self.edges = edges

		SEED = 56427
		random.seed(SEED)

		# Add nodes and edges
		for node in nodes:
			self.graph.AddNode(node)
		for edge in edges:
			self.graph.AddEdge(edge[0],edge[1])

	# Recommend friends based on the Common Neighbours
	def recommend_friends_CN(self, node_id, n_rec):
		scores = []
		for node in self.graph.Nodes():
			node = node.GetId()
			neighbours = snap.TIntV()
			# don't take into account itself and those it's already connected to
			if node != node_id and not self.graph.IsEdge(node,node_id):
				scores.append([node, snap.GetCmnNbrs(self.graph,node,node_id,neighbours)])

		# Sort the list based on the first item (the score) - Descending
		# Then sort by the nodeId - Ascending
		scores.sort(key=lambda x: x[0])
		scores.sort(key=lambda x: x[1], reverse=True)
		# And print the first n_rec ones - Defaults to 10
		# If the number of items is < n_rec it'll just print them all.
		return scores[:n_rec]

	def recommend_friends_J(self, node_id, n_rec):
		"""
			Jaccard coefficient.
			--------------------
			For the numerator we will do the same as what we did for the Common Neighbours
			For the denominator we will add the number of neighbours of A to the number of
			neighbours of B and then subtract the number of common neighbours (ie. the numerator)
		"""
		scores = []
		neighbours_b = self.graph.GetNI(node_id).GetOutDeg()

		for node in self.graph.Nodes():
			# Get the number of neighbours for node and node_id
			neighbours_a = node.GetOutDeg()
			node = node.GetId()
			neighbours = snap.TIntV()
			if node != node_id and not self.graph.IsEdge(node,node_id):
				common = snap.GetCmnNbrs(self.graph,node,node_id,neighbours)
				union = neighbours_a + neighbours_b - common
				scores.append([node, common / float(union)])
		scores.sort(key=lambda x: x[0])
		scores.sort(key=lambda x: x[1], reverse=True)
		return scores[:n_rec]

	def recommend_friends_AA(self, node_id, n_rec):
		""" Adamic and Adar scoring similarity"""
		scores = []
		neighbours_b = self.graph.GetNI(node_id).GetOutDeg()
		for node in self.graph.Nodes():
			sum = 0
			# Get the number of neighbours for node and node_id
			node = node.GetId()
			neighbours = snap.TIntV()
			if node != node_id and not self.graph.IsEdge(node,node_id):
				snap.GetCmnNbrs(self.graph,node,node_id,neighbours)
				for c in neighbours:
					sum += 1 / math.log(self.graph.GetNI(c).GetOutDeg(),2)
				scores.append([node, sum])
		scores.sort(key=lambda x: x[0])
		scores.sort(key=lambda x: x[1], reverse=True)
		return scores[:n_rec]

	def recommend_friends_random(self, node_id, n_rec):
		""" Random recommendations """
		not_friends = set(self.nodes) - set(self.graph.GetNI(node_id).GetOutEdges())
		if n_rec > len(not_friends):
			n_rec = len(not_friends)
		return random.sample(not_friends,n_rec)

	def bonus_recommend_friends_preferencial(self, node_id, n_rec):
		""" Preferencial Attachment """
		scores = []
		num_friends = len(list(self.graph.GetNI(node_id).GetOutEdges()))
		# Iterate through all the nodes
		for node in self.graph.Nodes():
			# Get the number of neighbours for node and node_id
			p_node = node.GetId()
			if p_node != node_id and not self.graph.IsEdge(p_node,node_id):
				p_num_friends = len(list(node.GetOutEdges()))
				scores.append([p_node, num_friends * p_num_friends])
		scores.sort(key=lambda x: x[0])
		scores.sort(key=lambda x: x[1], reverse=True)
		return scores[:n_rec] 

	def del_edge(self,source,dest):
		""" Removes an edge from the graph """
		self.graph.DelEdge(source,dest)

	def add_edge(self,source,dest):
		""" Adds an edge to the graph """
		self.graph.AddEdge(source,dest)
