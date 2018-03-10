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

"""

SETTINGS = {
	'input_filename': '../facebook_combined.txt',
	'test_nodeIDs': [14, 35, 107, 1126],
	'rec_num': 10
}