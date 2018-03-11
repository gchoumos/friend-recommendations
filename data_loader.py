import re
import timeit

class DataLoader(object):
	""" """

	def __init__(self, filename="./facebook_combined.txt"):
		self.filename = filename

	def get_nodes(self,edges):
		"""
			Simple function to get the set of node ids appearing in the input file
		"""
		nodes = []

		for edge in edges:
			# edge = edge.split()
			nodes.append(int(edge[0]))
			nodes.append(int(edge[1]))

		print "nodes list length: %s" % str(len(nodes))

		return set(nodes)

	def get_edges_from_file(self):
		"""
			Get a list of the edges
		"""
		edges = []

		with open(self.filename) as f:
			lines = f.readlines()

		for line in lines:
			line = line.split()
			edges.append([int(line[0]),int(line[1])])

		return edges
