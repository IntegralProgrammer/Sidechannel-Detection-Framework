#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../../')

#-----------------------------------------------------------------------

import DataGatheringLayer


#-----------------------------------------------------------------------

import FeatureExtractionLayer

PCAP_EXAMPLE = "vnc_geany36_alphabet.pcap"

"""
Use the FeatureExtractionLayer to get all sequences of sizes of SSH
packet payloads and their corresponding plaintext labels.
"""
PLAIN_SRC = ("172.17.0.1", "*")
PLAIN_DST = ("172.17.0.3", 5900)

#CRYPTO_SRC = ("172.17.0.3", "*")
#CRYPTO_DST = ("172.17.0.2", 22)

#CRYPTO_SRC = ("172.17.0.2", 22)
#CRYPTO_DST = ("172.17.0.3", "*")

CRYPTO_SRC = ("172.17.0.2", "*")
CRYPTO_DST = ("172.17.0.3", "*")

#Label encrypted packets based on plaintext data
labeled_encrypted_events = FeatureExtractionLayer.get_pcap_ssh_encrypted_sequence(PCAP_EXAMPLE, PLAIN_SRC, PLAIN_DST, CRYPTO_SRC, CRYPTO_DST, DataGatheringLayer.vnc_rfb.key_event_tagger)

key_dict = {}

for datum in labeled_encrypted_events:
	print ""
	print "----------------------------------------"
	print datum
	print "----------------------------------------"
	print ""
	keypress = datum[0][1]
	bytes_exchanged = sum(datum[1])
	if keypress not in key_dict:
		key_dict[keypress] = []
	
	key_dict[keypress].append(bytes_exchanged)


print ""
print ""

for k in "abcdefghijklmnopqrstuvwxyz":
	print "{}: {}".format(k, key_dict[k])

simplified_labels = []
simplified_data = []

for k in "abcdefghijklmnopqrstuvwxyz":
	for n in key_dict[k]:
		simplified_labels.append(k)
		simplified_data.append([n])

#-----------------------------------------------------------------------

import MachineLearningLayer

model_training_data, model_training_labels, model_test_data, model_test_labels = MachineLearningLayer.split_data_balanced_labels(simplified_data, simplified_labels, 0.50)

#Debug printing
print " === Training Set ==="
for i in range(0, len(model_training_data)):
	print "{}: {}".format(model_training_labels[i], model_training_data[i])
print ""

#Debug printing
print " === Testing Set ==="
for i in range(0, len(model_test_data)):
	print "{}: {}".format(model_test_labels[i], model_test_data[i])
print ""

#Create the machine-learning adversary model
adversary_model = MachineLearningLayer.make_decision_tree_model(model_training_data, model_training_labels, model_test_data, model_test_labels)

print adversary_model
print ""

#-----------------------------------------------------------------------

import ThreatModellingLayer

adv_performances = {}

for k in "abcdefghijklmnopqrstuvwxyz":
	adv_performances[k] = ThreatModellingLayer.vnc_over_ssh.evaluate_key_type_prediction(adversary_model, k)

alphabet = []
perfs = []
for k in "abcdefghijklmnopqrstuvwxyz":
	alphabet.append(k)
	perfs.append(100*adv_performances[k])
	print "ADVPERF({}) = {}".format(k, adv_performances[k])


#-----------------------------------------------------------------------

import ReactiveLayer

#Create the object of the report webpage
report_webpage = ReactiveLayer.ReportWebpage()

#Create a graph of the predictability of each character
ReactiveLayer.bar_graph.render_bar_graph(0, 100, alphabet, perfs, "Key Press", "Probability of Successful Prediction (%)", "/www/ssh_keypress_predict.png")

#Add this information to the report webpage
report_webpage.add_infocard("Adversary Score for Predicting Keypress", "/ssh_keypress_predict.png")

#Render the HTML page
report_webpage.render_html("/www/index.html")

