#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def trials_for_case(sc_case, alphabet_size, strlen):
	"""
	Break sc_case into segments. This transforms sc_case into the points
	along the password length where the side-channel behavior described
	by sc_case occurs.
	"""
	sc_points = []
	for i in range(len(sc_case)):
		if sc_case[i] == '1':
			sc_points.append(int((strlen * i) / float(len(sc_case))))
	
	expected_trials = 0
	prev_pt = 0
	for pt in sc_points:
		this_dist = pt - prev_pt
		expected_trials += (alphabet_size ** this_dist) / 2
		prev_pt = pt
	
	#...and the distance from prev_pt to the end
	this_dist = strlen - prev_pt
	expected_trials += (alphabet_size ** this_dist) / 2
	
	return expected_trials

def toSwitches(n, l):
	pattern = "{:b}".format(n)
	while len(pattern) < l:
		pattern = '0' + pattern
	
	return pattern

def calculate_string_entropy(machinelearning_model, alphabet_size, strlen):
	"""
	- Go through the labels in adv_mdl.
		- How well can we predict that the first 0% of bits are correct?
		- How well can we predict that the first 10% of bits are correct?
		- How well can we predict that the first 20% of bits are correct?
		...
		- How well can we predict that the first 90% of bits are correct?
		- How well can we predict that the first 100% of bits are correct?
		
	- If there are 10 symbols in the alphabet and the string has a
		length of 6, the string can be guessed in a maximum of
		10^6 (1 000 000) guesses.
	
	- If we have a side-channel that will let us know if the first 3
		symbols are correct then...
		
		- We can guess the first 3 symbols in a maximum of 10^3 (1000)
			trials.
		
		- We can guess the second 3 symbols in a maximum of 10^3 (1000)
			trials.
		
		- Therefore we can guess the string in a maximum of 2000 trials.
		
	- Suppose...
		
		- We can guess with an accuracy of 70% the first 3 symbols in a
			maximum of 10^3 (1000) trials.
		
		- In an expected 500 trials we can be 70% confident of the first
			3 symbols.
		
		- Therefore we have two cases:
			- Side-channel works:
				500 + 500
			- Side-channel does not work:
				500,000
			
			- With this side-channel we can have the password cracked in
				an estimated 0.70*(500+500) + 0.30*(500000) = 150,700 trials
	"""
	
	#Get the complete list of password length guesses
	guess_length = []
	
	for pair in machinelearning_model['evaluation_run']:
		ground_truth = pair[0]
		if ground_truth not in guess_length:
			guess_length.append(ground_truth)
		
	guess_length.sort()
	
	guess_probs = []
	for gl in guess_length:
		tp = 0
		fp = 0
		len_count = 0
		not_len_count = 0
		#Require: P(Signal | Length)...psl
		#Require: P(Length)...pl
		#Require: P(Signal | DifferentLength)...pdsl
		#Require: P(DifferentLength)...pdl
		for pair in machinelearning_model['evaluation_run']:
			ground_truth = pair[0]
			pred_val = pair[1]
			if pred_val == gl and ground_truth == gl:
				tp += 1
			
			elif pred_val == gl and ground_truth != gl:
				fp += 1
			
			if ground_truth == gl:
				len_count += 1
			else:
				not_len_count += 1
		
		psl = float(tp) / float(len_count)
		pl = float(len_count) / float(len_count + not_len_count)
		psdl = float(fp) / float(not_len_count)
		pdl = float(not_len_count) / float(len_count + not_len_count)
		
		#Apply Bayes Rule
		if psl*pl == 0:
			guess_probs.append(0)
		else:
			guess_probs.append((psl*pl)/ ((psl*pl) + (psdl*pdl)))
		
		#guess_probs.append(float(tp)/float(tp + fp))
	
	
	#Do a binary count from 0 to len(guess_length)
	n_categories = len(guess_length)
	
	total_expected_trials = 0
	for bval in range(0, (2**n_categories)):
		sc_case = toSwitches(bval, len(guess_length))
		expected_trials = trials_for_case(sc_case, alphabet_size, strlen)
		case_prob = 1.0
		
		for bit_i in range(len(sc_case)):
			bit = sc_case[bit_i]
			if bit == '0':
				case_prob = case_prob * (1.0 - guess_probs[bit_i])
			elif bit == '1':
				case_prob = case_prob * guess_probs[bit_i]
		
		cp_num = case_prob.as_integer_ratio()[0]
		cp_den = case_prob.as_integer_ratio()[1]
		total_expected_trials += int(cp_num * expected_trials) / int(cp_den)
	
	return math.log(2*total_expected_trials, 2)
