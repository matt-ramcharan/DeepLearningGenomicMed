# DeepLearningGenomicMed

## Todo

Multitask on toy problems

Cosmic data manipulate

Write a lot about data.

Build Support vector machine as base for data

Finding similarites between cancers
Type code is a clinical catogorisation.

FATHMM-XF should be used for cancer data.

CScape using same base information. Different information is cancer type, which is a task.

Choosing which are functional disease

Same variant 5 or more times was a driver.
If absent its neutral

numbers of postiives at recurrence levels agree with Cscape

Cscape was 76% ish up to 90% raise by 3% with multitask

non cancer very conserved is good

cancer highly successful cell. able to proliferate in a poor situation. Hypoxic. Survivor. 
conserved vs not conserved different from standard cell.


HAVE UNTIL 5pm WEDNESDAY - INTERIM REPORT.

## Plan

current progress understanding of models

Need a strong plan.

A lot of data manipulation

Check for recurrence in CScape data

Build Support vector machine as base for data (1 task, 1 kernel)

1 task, multikernel learning (Following FATHMM-MKL (effectively CScape - MKL, if somewhat novel))

Focus on getting multitask working on toy data 

Multitask on cscape (novel)



What tring to do
steps to get upto
differences in methods
weeks worth of work per task

build
analyse
build
analyse
build
analyse
Big Anaylse



Contact Mark Rogers 

Make own version of multitask.




## Notes
Communicate with Mark Rogers in Collerado
[mark.f.rogers.phd@gmail.com](mark.f.rogers.phd@gmail.com)


Sequence convervation across different data types

labelling of variance from Cosmic Dataset (used ot train CSCape) cancer.sanger.ac.uk/cosmic.

International Cancer Genome Consoritum data


sequence conversation, histime the same

what changes is what is designated as a driver.
CScape paper - "positives and negatives"
positives = all cancers

eg. breast cancer fewer cases. fewer positives.

Task = type of cancer

different recurrence levels of cancers

## Original Task

Project title: Deep learning methods in genomic medicine

Primary supervisor: Colin Campbell

Co-supervisor(s):

Level: BEng or MEng

Project description (including the motivating real-world problem and stakeholders):
Within genomic medicine there is significant interest in using advanced data analysis methods from
areas such as machine learning, to interpret whole genome, and related (‘omics’) datasets. There are many applications of machine learning in these contexts including the identification of disease-drivers, predicting the best therapeutic agent, through to identification of novel disease categories.

In recent years, within the machine learning community, there has been significant interest in deep
learning methods. The most well known of these are deep neural network learning methods which
are implemented in packages such as Tensorflow. Deep neural networks have been used extensively
in application areas such as machine vision (e.g. for self-driving car technologies) and in natural
language processing. Some similar methods have been proposed which do not use multi-layered
neural networks been retain the deep learning architecture. 

In the first part of this project we will investigate some of these alternatives, such as Deep Forest and Deep SVMs and perform a comparative study of generalisation performance on benchmarking datasets from the UCI Machine Learning Repository. After this initial phase, when we become familiar with these methods, we will apply them to medical genomic datasets in which the goal is to predict the pathogenic impact of variation in the human genome. The goal of this project is therefore to understand which type of methodology gives best test accuracy on novel data and to use the best such method on the important task of predicting the functional consequences of variants in the human genome.
