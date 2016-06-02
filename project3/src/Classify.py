from Helper import *
from sklearn import svm

def train_svm(data_vecs, labels, kernel_type):
	""" Train the linear classification model. Here LinearSVC from Scikit is used.

		Input: 
		Data_vecs: List of feature vectors
		Labels: labels of the feature vectors (1 or -1)

		Output:
		Trained weights, example of format for 3 features: 
		[[ 0.43478193  0.43478193  0.43478193]]

	"""

	clf = svm.SVC(kernel=kernel_type)
	clf.fit(data_vecs, labels)
	weights = clf.coef_
	#dec=clf.decision_function()
	#print dec

	return weights

#Helper.train_svm = train_svm

if __name__ == '__main__':
	#H = Helper()
	X = [[0, 0, 0], [1, 1, 1]]
	y = [0, 1]
	kernel_types = ['linear', 'rbf']

	for kernel_type in kernel_types:
		print 'Kernel type: ', kernel_type
		weights = train_svm(X, y, kernel_type)
	print weights