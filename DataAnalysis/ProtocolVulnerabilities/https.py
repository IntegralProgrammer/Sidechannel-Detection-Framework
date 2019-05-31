#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Describes everything that could be discovered in an HTTPS web browsing
session.

Important to note that we are only concerned with predicted labels
here. How the labels were predicted or how the data was gathered to
generate the predictions are outside the scope of this layer and are
the responsibilities of lower layers.
"""

def evaluate_form_result_prediction(machinelearning_model, specific_result):
	print "Running HTTPS form result prediction for result: {}".format(specific_result)
	#TODO: Implement me!

def evaluate_page_loaded_prediction(machinelearning_model, specific_url):
	print "Running HTTPS website visited prediction for URL: {}".format(specific_url)
	tp_count = 0
	fp_count = 0
	for pair in machinelearning_model['evaluation_run']:
		ground_truth = pair[0]
		predicted_value = pair[1]
		if str(ground_truth['url']) == specific_url:
			if str(predicted_value['url']) == specific_url:
				tp_count += 1
			else:
				fp_count += 1
	
	return float(tp_count) / float(tp_count + fp_count)

