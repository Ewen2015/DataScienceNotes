from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from .Report import Report

class Baseline(object):
	"""docstring for Baseline"""
	def __init__(self, data, target, features):
		super(Baseline, self).__init__()
		self.data = data
		self.target = target
		self.features = features

		self.train, self.test = train_test_split(data, test_size=0.2, random_state=0)

	def LR(self, feature_num=6):

		predictors=[]
		logreg_fs = LogisticRegression()
		rfe = RFE(logreg_fs, feature_num)
		rfe = rfe.fit(self.data[self.features], self.data[self.target])
		for ind, val in enumerate(rfe.support_):
			if val: predictors.append(self.features[ind])

		logreg = LogisticRegression()
		logreg.fit(self.train[predictors], self.train[self.target])

		rpt = Report(logreg, self.train, self.test, self.target, predictors)
		rpt.ALL()

		return None
	
	def RF(self):
		pass

