"""
	Settings file for our exercise
	------------------------------
	* input_filename
		the name of the file that we are going to get the edges from. It defaults to the
		filename that we got straight from the SNAP dataset after untarring it.
		https://snap.stanford.edu/data/egonets-Facebook.html
		Notice that it will be treated as a relative path. In the unlikely scenario that
		you might want this to take into account a file that is in a different directory,
		then you should also prepend whatever is required so that you get the
		relative/absolute path.

	* test_nodeIDs
		the node ids which are mentioned in the assignment for the recommendation checks

	* recommendation_num
		the number of recommendations to return. Defaults to a maximum of 10 as the
		assignment requires.

	* multiples
		for the evaluation part of the exercise we want to get node ids that are
		multiples of 100. So this is the default value. However, it can be changed
		to whatever you like (not fail-proof yet though so give it reasonable values).

	* experiments
		the number of times to conduct the experiment of removing a random edge and then
		suggesting neighbours to evaluate the models performance

"""

SETTINGS = {
	'input_filename': '../facebook_combined.txt',
	'test_nodeIDs': [14, 35, 107, 1126],
	'rec_num': 10,
	'multiples': 100,
	'experiments': 100
}