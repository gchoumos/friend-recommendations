"""
	TODO:
		-	We might probably want to use the DataLoader constructor in order to both
			get the nodes as well the edges. Or maybe not. My initial thought on this
			is to have the constructor of the DataLoader to call the corresponding
			procs. But I'm not yet sure about this and whether I prefer it or not.
		-	If using snap is eventually acceptable, add instructions for installation
			in the README.md file.
		-	Mention the terminaltables installation as well in the README.md (through pip).

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
from terminaltables import AsciiTable
from terminaltables import SingleTable

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

		# Show the results for different methods in parallel
		print "Common Friends method computation ..."
		rec_common = un_graph.recommend_friends_CN(node,n_recs)
		print "Jaccard method computation ..."
		rec_jaccard = un_graph.recommend_friends_CN(node,n_recs)
		print "Adamic & Adar method computation ..."
		rec_aa = un_graph.recommend_friends_AA(node,n_recs)

		_print_result_tables(node,'Common Friends',rec_common)
		_print_result_tables(node,'Jaccard',rec_jaccard)
		_print_result_tables(node,'Adamic & Adar',rec_aa)


def _print_result_tables(node,method,recs):
	"""
		This function aims to do a fancy printing of the results into
		ascii tables. Don't get too excited though. We could also do
		pipe this to a cowsay for the swag.

		Arguments:
		- node:	  node id for which we are recommending.
		- method: name of the method
		- recs:   actual recommendations of this method
	"""
	table_data = [['Rank','NodeID','Score']]
	for i in range(len(recs)):
		table_data.append([i+1,recs[i][0],recs[i][1]])

	table = SingleTable(table_data)
	table.justify_columns[0] = 'right'
	table.justify_columns[1] = 'right'
	table.justify_columns[2] = 'right'

	print "\n{0} - Recommendations for Node: {1}".format(method,node)
	print table.table

if __name__ == '__main__':
    main()