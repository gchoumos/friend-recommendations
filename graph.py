import snap

class UNGraph(object):
	""" Undirected Graph class """

	# Use snap's TUNGraph
	# This means that we won't have to add each edge twice (one for each direction)
	graph = snap.TUNGraph.New()

	def __init__(self, nodes=[], edges=[]):
		self.nodes = nodes
		self.edges = edges
		# Add the nodes
		for node in nodes:
			self.graph.AddNode(node)
		# Add the edges
		for edge in edges:
			self.graph.AddEdge(edge[0],edge[1])

	# Recommend friends based on the Common Neighbours
	def recommend_friends_CN(self, node_id, n_rec):
		scores = []
		# Iterate through all the nodes
		for node in self.graph.Nodes():
			node = node.GetId()
			neighbours = snap.TIntV()
			# don't take into account itself and those it's already connected to
			if node != node_id and not self.graph.IsEdge(node,node_id):
				#print "Nodes {0} and {1}: GOOD".format(node,node_id)
				scores.append([node, snap.GetCmnNbrs(self.graph,node,node_id,neighbours)])
				#print "Nodes {0} and {1}: GOOD - Score: {2}".format(node,node_id,snap.GetCmnNbrs(self.graph,node,node_id,neighbours))
			else:
				#print "Nodes {0} and {1}: BAD".format(node,node_id)
				pass

		# Sort the list based on the first item (the score) - Descending
		# Then sort by the nodeId (Ascending)
		scores.sort(key=lambda x: x[0])
		scores.sort(key=lambda x: x[1], reverse=True)
		# And print the first n_rec ones - Defaults to 10
		# If the number of items is < n_rec it'll just print them all.
		return scores[:n_rec]

