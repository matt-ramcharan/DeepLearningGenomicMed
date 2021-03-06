# import numpy as np
# import shogun
# from shogun.Features import LibSVM
# from shogun.Kernel import *
# from shogun.Classifier import AccuracyMeasure
# from shogun.Evaluation import RealFeatures, BinaryLabels, AccuracyMeasure
# from shogun.Kernel import GaussianKernel
import pandas as pd
from shogun.Loss import L2R_L2LOSS_SVC
import matplotlib.pyplot as plt
from shogun.Evaluation import RealFeatures, BinaryLabels, LibSVM, AccuracyMeasure, ROCEvaluation
import numpy as np
from shogun.Kernel import GaussianKernel, LibLinear

#MultiTask Dataset (reduced)
# train_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/train_alt.npy')
# test_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/test_alt.npy')

#Ratsh Dataset
train_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/train.npy')
test_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/test.npy')

np.apply_along_axis(np.random.shuffle, 1, train_data)
np.apply_along_axis(np.random.shuffle, 1, test_data)

#SVM just first task
train_feats = train_data[1, :, :-1]
test_feats = test_data[1, :, :-1]
train_label = train_data[1, :, -1]
test_label = test_data[1, :, -1]

# #Test Train Swap
# train_feats = test_data[1, :, :-1]
# test_feats = train_data[1, :, :-1]
# train_label = test_data[1, :, -1]
# test_label = train_data[1, :, -1]


features_train = RealFeatures(train_feats.T)
features_test = RealFeatures(test_feats.T)
labels_train = BinaryLabels(train_label.T)
labels_test = BinaryLabels(test_label.T)
epsilon = 0.001
# C = 1.0
C = 10000

# Gaussian
gauss_kernel = GaussianKernel(features_train, features_train, 2)

svm = LibSVM(C, gauss_kernel, labels_train)

# #Linear
# svm = LibLinear(C, features_train, labels_train)
# svm.set_liblinear_solver_type(L2R_L2LOSS_SVC)

# svm.set_epsilon(epsilon)

svm.train()


labels_predict = svm.apply(features_test)

alphas = svm.get_alphas()
b = svm.get_bias()

eval = AccuracyMeasure()


# accuracy = eval.evaluate(labels_predict.get_labels(), labels_test)
# print(accuracy)

eval.evaluate(labels_predict,labels_test)
accuracy=eval.get_accuracy()*100
# auc = eval.AUC()
print('Alphas:', alphas)
print('Bias:', b)
print('Accuracy(%):', accuracy)
