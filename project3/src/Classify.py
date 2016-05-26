from Helper import *
from sklearn import svm

def train_svm(self, data_vecs, labels):
	""" Train the linear classification model. Here LinearSVC from Scikit is used.

		Input: 
		Data_vecs: List of feature vectors
		Labels: labels of the feature vectors (1 or -1)

		Output:
		Trained weights, example of format for 3 features: 
		[[ 0.43478193  0.43478193  0.43478193]]

	"""

	clf = svm.LinearSVC()
	clf.fit(data_vecs, labels)
	weights = clf.coef_

	return weights

Helper.train_svm = train_svm

if __name__ == '__main__':
	H = Helper()
	X = [[0, 0, 0], [1, 1, 1]]
	y = [0, 1]
	weights = H.train_svm(X, y)
	print weights