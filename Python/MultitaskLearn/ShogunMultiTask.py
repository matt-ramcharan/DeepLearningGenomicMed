import shogun
import pandas as pd
import numpy as np

# from subprocess import Popen, PIPE
#
# def bgzip(filename):
#     """Call bgzip to compress a file."""
#     Popen(['bgzip', '-f', filename])
#
# def tabix_index(filename,
#         preset="gff", chrom=1, start=4, end=5, skip=0, comment="#"):
#     """Call tabix to create an index for a bgzip-compressed file."""
#     Popen(['tabix', '-p', preset, '-s', chrom, '-b', start, '-e', end,
#         '-S', skip, '-c', comment])
#
# def tabix_query(filename, chrom, start, end):
#     """Call tabix and generate an array of strings for each line it returns."""
#     query = '{}:{}-{}'.format(chrom, start, end)
#     process = Popen(['tabix', '-f', filename, query], stdout=PIPE)
#     for line in process.stdout:
#         yield line.strip().split()


#data = pd.read_csv('~/Documents/TechnicalProject/Data/cscape/cscape_coding_training_examples.tab', sep='\t')
#print(data)

neg_dataset = np.loadtxt("neg_dataset.csv",delimiter=',')
pos_dataset = np.loadtxt("pos_dataset.csv",delimiter=',')

