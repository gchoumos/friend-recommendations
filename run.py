"""
	TODO:
		-	We might probably want to use the DataLoader constructor in order to both
			get the nodes as well the edges. Or maybe not. My initial thought on this
			is to have the constructor of the DataLoader to call the corresponding
			procs. But I'm not yet sure about this and whether I prefer it or not.
		-	If using snap is eventually acceptable, add instructions for installation
			in the README.md file.

	THOUGHTS:
		-	I don't think we have to do anything twice as instructed by the assignment
			description to make an undirected graph. We can use the TUNGraph for this
			purpose.s
"""

from settings import SETTINGS
import snap
import random
from data_loader import DataLoader
from graph import UNGraph

nodes = set()
edges = set()

def main():
	print("Starting app...")

	data = DataLoader(SETTINGS['input_filename'])

	# Get the edges from the input file
	edges = data.get_edges_from_file()
	print "Edges set length (unique): %s" % str(len(edges))
	print "10 random items from the set:\n"
	print random.sample(edges,10)

	# Get the nodes from the input file
	nodes = data.get_nodes(edges)
	print "nodes set length (unique): %s" % str(len(nodes))
	print "10 random items from the set:\n"
	print random.sample(nodes,10)

	# Create the undirected graph
	print "Creating the undirected graph ..."
	un_graph = UNGraph(nodes,edges)

	for node in SETTINGS["test_nodeIDs"]:
		print "Computing recommended friendships for node {0} ...".format(node)
		n_recs = SETTINGS["rec_num"]

		# Print them a bit more nicely than just throwing them on screen
		print "Common Friends method"
		print "---------------------"
		print "Node\t\tScore"
		for recommendation in un_graph.recommend_friends_CN(node, n_recs):
			print "{0}\t{1}".format(recommendation[0],recommendation[1])

		print "Jaccard method"
		print "--------------"
		print "Node\t\tScore"
		for recommendation in un_graph.recommend_friends_J(node,n_recs):
			print "{0}\t{1}".format(recommendation[0],recommendation[1])

		print "Adamic & Adar method"
		print "--------------------"
		print "Node\t\tScore"
		for recommendation in un_graph.recommend_friends_AA(node,n_recs):
			print "{0}\t{1}".format(recommendation[0],recommendation[1])


if __name__ == '__main__':
    main()