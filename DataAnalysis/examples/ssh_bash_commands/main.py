#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- Feature Extraction Layer: Gets sequences of packets for given labels
- Machine Learning Layer: Uses a DecisionTree to map sequences to labels
- Threat Modelling Layer: Gets accuracy of command prediction
- Reactive Layer: Writes to a log file commands which can be accurately predicted
"""

import sys
sys.path.insert(0, '../../')

#-----------------------------------------------------------------------

import FeatureExtractionLayer

TAG_UDPPORT = 5006
SSH_STREAM_PORT = 22
PCAP_EXAMPLE = "capture_4.pcap"
LABELS_KEEP_LIST = ["command", "context"]

"""
Use the FeatureExtractionLayer to extract the labeled sequences of
encrypted network traffic.
"""
traffic_labels, traffic_data = FeatureExtractionLayer.get_pcap_labeled_sequences(PCAP_EXAMPLE, TAG_UDPPORT, SSH_STREAM_PORT)

#Debug printing
print " === Main List === "
for i in range(0,len(traffic_labels)):
	print "{}: {}".format(traffic_labels[i], traffic_data[i])
print ""

"""
Use the FeatureExtractionLayer to simplify the labels
"""
simplified_traffic_labels = list(FeatureExtractionLayer.filter_labels_list(traffic_labels, LABELS_KEEP_LIST))

#Debug printing
print " === Filtered List === "
for i in range(0, len(simplified_traffic_labels)):
	print "{}: {}".format(simplified_traffic_labels[i], traffic_data[i])
print ""


#-----------------------------------------------------------------------

import MachineLearningLayer

"""
Use the MachineLearningLayer to generate a predictive model for labels
given traffic patterns.
"""

#...but first split the data into training and test sets
model_training_data, model_training_labels, model_test_data, model_test_labels = MachineLearningLayer.split_data_balanced_labels(traffic_data, simplified_traffic_labels, 0.70)

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

#adversary_model = MachineLearningLayer.make_decision_tree_model(traffic_data, simplified_traffic_labels)
adversary_model = MachineLearningLayer.make_decision_tree_model(model_training_data, model_training_labels, model_test_data, model_test_labels)

#Debug printing
#print adversary_model

#-----------------------------------------------------------------------

import ThreatModellingLayer

"""
Use the ThreatModellingLayer to determine how accurately an adversary
can predict an executed command. Please note that the generated
predictive model, adversary_model, at this point has already evaluated
itself against the provided testing data and labels.
"""
COMMAND_PREDICT = "pwd"

cmd_executed_predictability = ThreatModellingLayer.ssh.evaluate_command_prediction(adversary_model, COMMAND_PREDICT)


#-----------------------------------------------------------------------

import ReactiveLayer

"""
Use the ReactiveLayer to simply print warning messages whenever
cmd_executed_predictability exceeds WARNING_TRIGGER_THRESHOLD
"""

WARNING_TRIGGER_THRESHOLD = 0.5
WARNING_MESSAGE = "Execution of the '{}' command can be predicted.".format(COMMAND_PREDICT)

ReactiveLayer.simple_log_warning(WARNING_MESSAGE, WARNING_TRIGGER_THRESHOLD, cmd_executed_predictability)


"""
Use the ReactiveLayer to render a webpage with guages showing the
machine learning modelled adversary's sucess at expoliting the
side-channel cues.
"""

commands = ["pwd", "ls", "ls /dev"]

#Create the object of the report webpage
report_webpage = ReactiveLayer.ReportWebpage()

for cmd in commands:
	cmd_prob = ThreatModellingLayer.ssh.evaluate_command_prediction(adversary_model, cmd)
	print "CMD: {}, PROB: {}".format(cmd, cmd_prob)
	guage_name = "/img/Predict_CMD_{}.png".format(ReactiveLayer.calculate_sha256(cmd))
	ReactiveLayer.polar_guages.render_guage_image(0, 100, int(100*cmd_prob), "/www" + guage_name)
	
	#Add this information to the report webpage
	report_webpage.add_infocard("Adversary Score for Predicting Command: {}".format(cmd), guage_name)

#Render the HTML page
report_webpage.render_html("/www/index.html")


