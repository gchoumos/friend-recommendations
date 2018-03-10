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

		start_time = timeit.default_timer()
		for edge in edges:
			# edge = edge.split()
			nodes.append(edge[0])
			nodes.append(edge[1])
		elapsed = timeit.default_timer() - start_time
		print("Get nodes - Duration: {0}".format(elapsed))

		print("nodes list length: " + str(len(nodes)))

		return set(nodes)

	def get_edges_from_file(self):
		"""
			Get a list of the edges
		"""
		edges = []

		with open(self.filename) as f:
			lines = f.readlines()

		start_time = timeit.default_timer()
		for line in lines:
			edges.append(line.split())
		elapsed = timeit.default_timer() - start_time
		print("Get edges - Duration: {0}".format(elapsed))

		return edges