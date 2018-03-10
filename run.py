"""
	TODO:
		-	We might probably want to use the DataLoader constructor in order to both
			get the nodes as well the edges. Or maybe not. My initial thought on this
			is to have the constructor of the DataLoader to call the corresponding
			procs. But I'm not yet sure about this and whether I prefer it or not.

	THOUGHTS:
		-	I don't think we have to do anything twice as instructed by the assignment
			description to make an undirected
"""

from settings import SETTINGS
import snap
import random
from data_loader import DataLoader

nodes = set()
edges = set()

def main():
	print("Starting app...")

	data = DataLoader(SETTINGS['input_filename'])

	# Get the edges from the input file
	edges = data.get_edges_from_file()
	print("Edges set length (unique):" + str(len(edges)))
	print("10 random items from the set:\n")
	print(random.sample(edges,10))

	# Get the nodes from the input file
	nodes = data.get_nodes(edges)
	print("nodes set length (unique):" + str(len(nodes)))
	print("10 random items from the set:\n")
	print(random.sample(nodes,10))

if __name__ == '__main__':
    main()