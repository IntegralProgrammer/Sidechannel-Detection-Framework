#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn import tree

def get_all_indices(lst, val):
	for i in range(0, len(lst)):
		if lst[i] == val:
			yield i

"""
Split the dataset into two data sets of size ratios
training_split:testing_split while trying to maintain the same
proportions of labels across the two sets.
"""
def split_data_balanced_labels(traffic_data, traffic_labels, training_split):
	testing_split = 1.0 - training_split
	training_data = []
	training_labels = []
	test_data = []
	test_labels = []
	
	#First, sort the traffic_data by labels
	sorted_traffic = []
	sorted_labels = []
	unique_labels = []
	for lbl in traffic_labels:
		if lbl not in unique_labels:
			unique_labels.append(lbl)
	
	for unique_lbl in unique_labels:
		for i in range(0, len(traffic_data)):
			if traffic_labels[i] == unique_lbl:
				sorted_traffic.append(traffic_data[i])
				sorted_labels.append(traffic_labels[i])
	
	#Then, split each sorted_traffic/sorted_label according to the training_split ratio
	for unique_lbl in unique_labels:
		indices = list(get_all_indices(sorted_labels, unique_lbl))
		#Split the list of indices by training_split:testing_split
		midpoint = int(float(len(indices)) * training_split)
		training_indices = indices[:midpoint]
		testing_indices = indices[midpoint:]
		for train_ind in training_indices:
			training_data.append(sorted_traffic[train_ind])
			training_labels.append(sorted_labels[train_ind])
		
		for test_ind in testing_indices:
			test_data.append(sorted_traffic[test_ind])
			test_labels.append(sorted_labels[test_ind])
	
	return training_data, training_labels, test_data, test_labels

"""
Finds the minimum and maximum of the union of all data_lists.
Then, for each list in data_lists, a new list is yielded describing how
frequent each number is.
"""
def make_entity_histogram(data_lists):
	min_val = None
	max_val = None
	for data_lst in data_lists:
		if len(data_lst) == 0:
			continue
		if min_val == None:
			min_val = min(data_lst)
		if max_val == None:
			max_val = max(data_lst)
		
		if min(data_lst) < min_val:
			min_val = min(data_lst)
		
		if max(data_lst) > max_val:
			max_val = max(data_lst)
		
	for data_lst in data_lists:
		hist = []
		for sz in range(min_val, max_val+1):
			hist.append(data_lst.count(sz))
		
		yield hist


def make_label_mapping(data_labels):
	unique_labels = []
	for lbl in data_labels:
		if lbl not in unique_labels:
			unique_labels.append(lbl)
	
	hashed_seq = []
	for lbl in data_labels:
		hashed_seq.append(unique_labels.index(lbl))
	
	return unique_labels, hashed_seq


def make_decision_tree_model(data_samples, data_labels, test_samples, test_labels):
	"""
	We acknowledge that the length of each profile may vary. Therefore,
	we create N decision trees where N is the number of unique profile
	lengths.
	"""
	unique_lengths = []
	for prof in data_samples:
		if len(prof) not in unique_lengths:
			unique_lengths.append(len(prof))
	
	"""
	Also, data_labels is a list of dictionaries and therefore each
	unique dictionary needs to be mapped to a number and then the
	mapping of numbers to entries returned.
	"""
	labels_mapping, remapped_labels = make_label_mapping(data_labels)
	
	#Create the classifiers
	classifiers = {}
	for unique_len in unique_lengths:
		classifiers[unique_len] = tree.DecisionTreeClassifier()
		training_data_subset = []
		training_labels_subset = []
		for i in range(0, len(data_samples)):
			if len(data_samples[i]) == unique_len:
				training_data_subset.append(data_samples[i])
				training_labels_subset.append(remapped_labels[i])
		
		classifiers[unique_len].fit(training_data_subset, training_labels_subset)
	
	machinelearning_model = {}
	machinelearning_model['classifiers'] = classifiers
	machinelearning_model['labels_mapping'] = labels_mapping
	machinelearning_model['evaluation_run'] = []
	
	#Evaluate the classifiers against test_samples, test_labels
	for i in range(0, len(test_samples)):
		true_val = test_labels[i]
		if len(test_samples[i]) not in classifiers.keys():
			machinelearning_model['evaluation_run'].append((true_val, "UNKNOWN"))
		else:
			pred_val = classifiers[len(test_samples[i])].predict([test_samples[i]])[0]
			machinelearning_model['evaluation_run'].append((true_val, labels_mapping[pred_val]))
	
	return machinelearning_model
