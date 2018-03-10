import snap

class UNGraph(object):
	""" Undirected Graph class """

	def __init__(self, nodes=[], edges=[]):
		# Use snap's TUNGraph
		graph = snap.TUNGraph.New()
		# Add the nodes
		for node in nodes:
			graph.AddNode(node)