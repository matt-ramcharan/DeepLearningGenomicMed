import shogun
import pandas as pd
import numpy as np

train_data = np.load('train.npy')
test_data = np.load('test.npy')
correlations = np.load('corr.npy')

# features_train = train_data[:,:,:-1]
# features_test = train_data[:,:,:-1]
# labels_train = train_data[:,:,-1]
# labels_test = test_data[:,:,-1]

features_train = train_data[1,:,:-1]
features_test = train_data[1,:,:-1]
labels_train = train_data[1,:,-1]
labels_test = test_data[1,:,-1]


## Multiple Kernel Learning
# poly_kernel = shogun.PolyKernel(10, 2)
# gauss_kernel_1 = shogun.GaussianKernel(2.0)
# gauss_kernel_2 = shogun.GaussianKernel(3.0)
#
# combined_kernel = shogun.CombinedKernel()
# combined_kernel.append_kernel(poly_kernel)
# combined_kernel.append_kernel(gauss_kernel_1)
# combined_kernel.append_kernel(gauss_kernel_2)
# combined_kernel.init(features_train, features_train)
#
# binary_svm_solver = shogun.SVRLight()
# mkl = shogun.MKLRegression(binary_svm_solver)
# mkl.set_kernel(combined_kernel)
# mkl.set_labels(labels_train)
# mkl.train()
#
# beta = combined_kernel.get_subkernel_weights()
# alpha = mkl.get_alphas()
#
# combined_kernel.init(features_train, features_test)
# labels_predict = mkl.apply_regression()
#
# combined_kernel.init(features_train, features_test)
# labels_predict = mkl.apply_regression()
