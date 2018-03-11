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
			purpose.
		-	After a few minutes of debate and discussions, we consider node id 0 as a
			multiple of 100 (100*0 = 0).
			Supporting evidence: http://mathforum.org/library/drmath/view/60913.html
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

	SEED = 56427
	random.seed(SEED)

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
		rec_jaccard = un_graph.recommend_friends_J(node,n_recs)
		print "Adamic & Adar method computation ..."
		rec_aa = un_graph.recommend_friends_AA(node,n_recs)

		_print_result_tables(node,'Common Friends',rec_common)
		_print_result_tables(node,'Jaccard',rec_jaccard)
		_print_result_tables(node,'Adamic & Adar',rec_aa)

	# Get the ids that are mutliples of the configured value (default: 100)
	node_multiples = [x for x in nodes if x%SETTINGS['multiples'] == 0]

	# For each of those node ids, get top 10 recommendations and scores
	# We keep both the full output of the recommendation computations as well
	# as the nodes separately in order to make our lives easier for the comparisons
	rec_results = {}
	same_all   = 0
	same_cn_j  = 0
	same_cn_aa = 0
	same_j_aa  = 0

	for node in node_multiples:
		rec_results[node] = {'cn':{},'j':{},'aa':{}}

		rec_results[node]['cn']['full']  = un_graph.recommend_friends_CN(node,n_recs)
		rec_results[node]['cn']['nodes'] = [x[0] for x in rec_results[node]['cn']['full']]

		rec_results[node]['j']['full']  = un_graph.recommend_friends_J(node,n_recs)
		rec_results[node]['j']['nodes'] = [x[0] for x in rec_results[node]['j']['full']]

		rec_results[node]['aa']['full'] = un_graph.recommend_friends_AA(node,n_recs)
		rec_results[node]['aa']['nodes'] = [x[0] for x in rec_results[node]['aa']['full']]

		# It is not really necessary to keep the boolean outcome of the results comparison
		# in the dict, but we keep it anyway.

		rec_results[node]['same_all'] =	rec_results[node]['cn']['nodes'] == \
										rec_results[node]['j']['nodes']  == \
										rec_results[node]['aa']['nodes']

		rec_results[node]['same_cn_j'] = rec_results[node]['cn']['nodes'] == \
										 rec_results[node]['j']['nodes']

		rec_results[node]['same_cn_aa'] = rec_results[node]['cn']['nodes'] == \
										  rec_results[node]['aa']['nodes']

		rec_results[node]['same_j_aa'] = rec_results[node]['j']['nodes'] == \
										 rec_results[node]['aa']['nodes']

		# This is very fancy
		same_all   += 1*rec_results[node]['same_all']
		same_cn_j  += 1*rec_results[node]['same_cn_j']
		same_cn_aa += 1*rec_results[node]['same_cn_aa']
		same_j_aa  += 1*rec_results[node]['same_j_aa']

	print "Comparison results for nodes with IDs being multiples " \
		  "of {0}".format(SETTINGS['multiples'])

	_print_comparisons(len(node_multiples), same_all, same_cn_j,same_cn_aa, same_j_aa)

	#####################################
	# Random removal and re-suggestions #
	#####################################

	avg_rank_common  = []
	avg_rank_jaccard = []
	avg_rank_aa      = []
	avg_rank_rnd     = []
	avg_rank_pref    = []
	# Perform the experiment the configured amount of times - Default: 100
	for i in range(SETTINGS['experiments']):
		# Randomly choose 1 of the friends
		F1 = random.choice(node_multiples)
		# Randomly choose 1 of its friends
		F2 = random.choice(list(un_graph.graph.GetNI(F1).GetOutEdges()))
		# print "F1 node id: {0}\tF2 node id: {1}".format(F1,F2)
		# print "Removing edge [{0},{1}] ...".format(F1,F2)
		un_graph.del_edge(F1,F2)

		# Compute friend recommendations after the edge deletion for both F1 and F2
		f1_rec_common  = [x[0] for x in un_graph.recommend_friends_CN(F1,n_recs)]
		f1_rec_jaccard = [x[0] for x in un_graph.recommend_friends_J(F1,n_recs)]
		f1_rec_aa      = [x[0] for x in un_graph.recommend_friends_AA(F1,n_recs)]
		f1_rec_rnd     = un_graph.recommend_friends_random(F1,n_recs)
		f1_rec_pref    = [x[0] for x in un_graph.bonus_recommend_friends_preferencial(F1,n_recs)]

		f2_rec_common  = [x[0] for x in un_graph.recommend_friends_CN(F2,n_recs)]
		f2_rec_jaccard = [x[0] for x in un_graph.recommend_friends_J(F2,n_recs)]
		f2_rec_aa      = [x[0] for x in un_graph.recommend_friends_AA(F2,n_recs)]
		f2_rec_rnd     = un_graph.recommend_friends_random(F2,n_recs)
		f2_rec_pref    = [x[0] for x in un_graph.bonus_recommend_friends_preferencial(F2,n_recs)]


		rank_common_f1 = rank_jaccard_f1 = rank_aa_f1 = rank_rnd_f1 = rank_pref_f1 = -1
		rank_common_f2 = rank_jaccard_f2 = rank_aa_f2 = rank_rnd_f2 = rank_pref_f2 = -1

		if F2 in f1_rec_common:
			rank_common_f1 = f1_rec_common.index(F2)
		if F2 in f1_rec_jaccard:
			rank_jaccard_f1 = f1_rec_jaccard.index(F2)
		if F2 in f1_rec_aa:
			rank_aa_f1 = f1_rec_aa.index(F2)
		if F2 in f1_rec_rnd:
			rank_rnd_f1 = f1_rec_rnd.index(F2)
		if F2 in f1_rec_pref:
			rank_pref_f1 = f1_rec_pref.index(F2)

		if F1 in f2_rec_common:
			rank_common_f2 = f2_rec_common.index(F1)
		if F1 in f2_rec_jaccard:
			rank_jaccard_f2 = f2_rec_jaccard.index(F1)
		if F1 in f2_rec_aa:
			rank_aa_f2 = f2_rec_aa.index(F1)
		if F1 in f2_rec_rnd:
			rank_rnd_f2 = f2_rec_rnd.index(F1)
		if F1 in f2_rec_pref:
			rank_pref_f2 = f2_rec_pref.index(F1)

		# We won't even consider the random reccommendation here or the bonus ones
		# or they'll destroy our metrics.
		if rank_common_f1 == -1 or rank_common_f2 == -1 \
			or rank_jaccard_f1 == -1 or rank_jaccard_f2 == -1 \
			or rank_aa_f1 == -1 or rank_aa_f2 == -1:
			un_graph.add_edge(F1,F2)
			continue

		avg_rank_common.append((rank_common_f1 + rank_common_f2) / 2.0)
		avg_rank_jaccard.append((rank_jaccard_f1 + rank_jaccard_f2) / 2.0)
		avg_rank_aa.append((rank_aa_f1 + rank_aa_f2) / 2.0)
		if rank_rnd_f1 != -1 and rank_rnd_f2 != -1:
			avg_rank_rnd.append((rank_rnd_f1 + rank_rnd_f2) / 2.0)
		if rank_pref_f1 != -1 and rank_pref_f2 != -1:
			avg_rank_pref.append((rank_pref_f1 + rank_pref_f2) / 2.0)


		un_graph.add_edge(F1,F2)


	print "Total Successful Experiments"
	print "----------------------------"
	print "Common Hits: {0}".format(len(avg_rank_common))
	print "Common Avg Rank: {0}".format(sum(avg_rank_common)/float(len(avg_rank_common)))
	print "Jaccard Hits: {0}".format(len(avg_rank_jaccard))
	print "Jaccard Avg Rank: {0}".format(sum(avg_rank_jaccard)/float(len(avg_rank_jaccard)))
	print "AA Hits: {0}".format(len(avg_rank_aa))
	print "AA Avg Rank: {0}".format(sum(avg_rank_aa)/float(len(avg_rank_aa)))
	print "(Bonus) Preferencial Attachment Hits: {0}".format(len(avg_rank_pref))
	if len(avg_rank_pref) != 0:
		print "(Bonus) Preferencial Attachment Avg Rank: {0}".format(sum(avg_rank_pref)/float(len(avg_rank_pref)))
	else:
		print "(Bonus) Preferencial Attachment Avg Rank: Infinity (which is bad)"
	print "Random Hits: {0}".format(len(avg_rank_rnd))
	if len(avg_rank_rnd) != 0:
		print "Random Avg Rank: {0}".format(sum(avg_rank_rnd)/float(len(avg_rank_rnd)))
	else:
		print "Random Avg Rank: Infinity (which is bad)"

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
	table.justify_columns[2] = 'left'

	print "\n{0} - Recommendations for Node: {1}".format(method,node)
	print table.table

def _print_comparisons(multiples_len, s_all, s_cn_j, s_cn_aa, s_j_aa):
	table_data = [['','Same','Total','Percentage']]
	table_data.append(['ALL',s_all,multiples_len,100*s_all/float(multiples_len)])
	table_data.append(['CN - J',s_cn_j,multiples_len,100*s_cn_j/float(multiples_len)])
	table_data.append(['CN - AA',s_cn_aa,multiples_len,100*s_cn_aa/float(multiples_len)])
	table_data.append(['J  - AA',s_j_aa,multiples_len,100*s_j_aa/float(multiples_len)])

	avg_all = 100*((s_cn_j+s_cn_aa+s_j_aa)/(3*float(multiples_len)))
	table_data.append(['Avg Similarity','-','-',avg_all])

	table = SingleTable(table_data)
	table.inner_footing_row_border = True

	print "Fancy results table:"
	print table.table

if __name__ == '__main__':
    main()