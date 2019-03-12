# import numpy as np
# import shogun
# from shogun.Features import LibSVM
#from shogun.Kernel import *
# from shogun.Classifier import AccuracyMeasure
# from shogun.Evaluation import RealFeatures, BinaryLabels, AccuracyMeasure
# from shogun.Kernel import GaussianKernel
from shogun.Evaluation import RealFeatures, BinaryLabels, LibSVM, AccuracyMeasure
import numpy as np
from numpy.random import randn
from shogun.Kernel import GaussianKernel


train_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/train.npy')
test_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/test.npy')

train_feats = train_data[1, :, :-1]
test_feats = test_data[1, :, :-1]
train_label = train_data[1, :, -1]
test_label = test_data[1, :, -1]

features_train = RealFeatures(train_feats.T)
features_test = RealFeatures(test_feats.T)
labels_train = BinaryLabels(train_label.T)
labels_test = BinaryLabels(test_label.T)
epsilon = 0.001
C = 1.0
#
gauss_kernel = GaussianKernel(features_train, features_train, 2)

svm = LibSVM(C, gauss_kernel, labels_train)
#svm.set_epsilon(epsilon)

svm.train()


labels_predict = svm.apply_binary(features_test)

alphas = svm.get_alphas()
b = svm.get_bias()

eval = AccuracyMeasure()

accuracy = eval.evaluate(labels_predict, labels_test)
print(accuracy)