# import numpy as np
# import shogun
# from shogun.Features import LibSVM
#from shogun.Kernel import *
# from shogun.Classifier import AccuracyMeasure
# from shogun.Evaluation import RealFeatures, BinaryLabels, AccuracyMeasure
# from shogun.Kernel import GaussianKernel
#from shogun import *
from shogun.Evaluation import RealFeatures, BinaryLabels, LibSVM, AccuracyMeasure, ROCEvaluation
import numpy as np
from numpy.random import randn
from shogun.Kernel import GaussianKernel, CombinedKernel, MKLClassification
import matplotlib.pyplot as plt
#from shogun import SVMLight


# train_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/train.npy')
# test_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/test.npy')

#MultiTask Dataset (reduced)
train_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/train_alt.npy')
test_data = np.load('/home/matt/Documents/TechnicalProject/DeepLearningGenomicMed/Python/MultitaskLearn/test_alt.npy')


np.apply_along_axis(np.random.shuffle, 1, train_data)
np.apply_along_axis(np.random.shuffle, 1, test_data)

# train_feats = train_data[1, :, :-1]
# test_feats = test_data[1, :, :-1]
# train_label = train_data[1, :, -1]
# test_label = test_data[1, :, -1]

# #Tasks concatenated
test_data = np.reshape(test_data, [64000, 101])
train_data = np.reshape(train_data, [640, 101])

train_feats = train_data[:, :-1]
test_feats = test_data[:, :-1]
train_label = train_data[:, -1]
test_label = test_data[:, -1]

features_train = RealFeatures(train_feats.T)
features_test = RealFeatures(test_feats.T)
labels_train = BinaryLabels(train_label.T)
labels_test = BinaryLabels(test_label.T)
epsilon = 0.001
C = 100000

combined_kernel = CombinedKernel()

#gauss_kernel_1 = GaussianKernel(features_train, features_train, 15)
gauss_kernel_1 = GaussianKernel(features_train, features_train, 2)
gauss_kernel_2 = GaussianKernel(features_train, features_train, 0.5)

combined_kernel.append_kernel(gauss_kernel_1)
combined_kernel.append_kernel(gauss_kernel_2)
combined_kernel.init(features_train, features_train)


libsvm = LibSVM()
svm = MKLClassification(libsvm)
svm.set_interleaved_optimization_enabled(False)
svm.set_kernel(combined_kernel)
svm.set_labels(labels_train)

svm.train()

beta = combined_kernel.get_subkernel_weights()
alpha = svm.get_alphas()

combined_kernel.init(features_train, features_test)
labels_predict = svm.apply()


#
# labels_predict = svm.apply(features_test)
# train_pred = svm.apply(features_train)
# alphas = svm.get_alphas()
# b = svm.get_bias()
#
eval = AccuracyMeasure()
# train_eval = AccuracyMeasure()
# # accuracy = eval.evaluate(labels_predict.get_labels(), labels_test)
# # print(accuracy)
# train_eval.evaluate(train_pred, labels_train)
# train_accuracy = train_eval.get_accuracy() * 100

eval.evaluate(labels_predict, labels_test)
accuracy = eval.get_accuracy() * 100

roc = ROCEvaluation()
roc_pred = roc.evaluate(labels_predict, labels_test)
test = roc.get_ROC()
plt.plot(test[0], test[1], marker='.')
plt.show()

print('Concatenated')
print('Alphas:', alpha)
print('Beta:', beta)
print('AUC:', roc_pred)
#
# print('Train Accuracy(%):', train_accuracy)
print('Accuracy(%):', accuracy)
