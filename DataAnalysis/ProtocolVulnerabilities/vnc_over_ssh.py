#!/usr/bin/env python
# -*- coding: utf-8 -*-

def evaluate_key_type_prediction(machinelearning_model, specific_keypress):
	print "Running Key Type prediction for key: {}".format(specific_keypress)
	tp_count = 0
	fp_count = 0
	for pair in machinelearning_model['evaluation_run']:
		ground_truth = pair[0]
		predicted_value = pair[1]
		
		if str(ground_truth) == specific_keypress:
			if str(predicted_value) == specific_keypress:
				tp_count += 1
			else:
				fp_count += 1
	
	return float(tp_count) / float(tp_count + fp_count)
