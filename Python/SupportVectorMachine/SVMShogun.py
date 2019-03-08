import numpy as np
import shogun
from shogun.Features import *
from shogun.Kernel import *
from shogun.Classifier import *
from shogun.Evaluation import *

train_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/train.npy')
test_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/test.npy')

features_train = RealFeatures(train_data[1, :, :-1])
features_test = RealFeatures(test_data[1, :, :-1])
labels_train = BinaryLabels(train_data[1, :, -1])
labels_test = BinaryLabels(test_data[1, :, -1])

C = 1.0
epsilon = 0.001
gauss_kernel = GaussianKernel(features_train, features_train, 15)

svm = LibSVM(C, gauss_kernel, labels_train)
svm.set_epsilon(epsilon)

svm.train()
labels_predict = svm.apply_binary(features_test)

alphas = svm.get_alphas()
b = svm.get_bias()

eval = AccuracyMeasure()
accuracy = eval.evaluate(labels_predict, labels_test)
