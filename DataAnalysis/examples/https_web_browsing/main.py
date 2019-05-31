#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- Feature Extraction Layer: Gets sequences of packets for given labels
- Machine Learning Layer: Uses a DecisionTree to map sequences to labels
- Threat Modelling Layer: Gets accuracy of form result prediction
- Reactive Layer: Writes to a log file results which can be accurately predicted
"""

import sys
sys.path.insert(0, '../../')

#Run deterministically
import numpy as np
np.random.seed(0)

#-----------------------------------------------------------------------

import FeatureExtractionLayer

TAG_UDPPORT = 5005
HTTPS_STREAM_PORT = 443
PCAP_EXAMPLE = "wikipedia_eval_09_17_2018.pcap"
LABELS_KEEP_LIST = ["url"]

"""
Use the FeatureExtractionLayer to extract the labeled sequences of
encrypted network traffic.
"""
traffic_labels, traffic_data = FeatureExtractionLayer.get_pcap_labeled_sequences(PCAP_EXAMPLE, TAG_UDPPORT, HTTPS_STREAM_PORT)

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

"""
Use the FeatureExtractionLayer to convert a list of payload sizes to a
list of approximate sizes of web objects.
"""

approx_webobj_sizes = []
for i in range(0, len(traffic_data)):
	this_approx = list(FeatureExtractionLayer.NBurst_detector(traffic_data[i], 1370))
	approx_webobj_sizes.append(this_approx)

#Debug printing
print " === Approximate Web Object Sizes === "
for i in range(0, len(simplified_traffic_labels)):
	print "{}: {}".format(simplified_traffic_labels[i], approx_webobj_sizes[i])
print ""

#-----------------------------------------------------------------------

import MachineLearningLayer

"""
Use the MachineLearningLayer to generate a predictive model for
labels (aka URLs) given traffic patterns.
"""

#...convert sizes list to sizes histogram
histogram_sizes = list(MachineLearningLayer.make_entity_histogram(approx_webobj_sizes))

#Consider also the count of objects downloaded in a session
for i in range(len(approx_webobj_sizes)):
	histogram_sizes[i].insert(0, len(approx_webobj_sizes[i]))

#...but first split the data into training and test sets
#model_training_data, model_training_labels, model_test_data, model_test_labels = MachineLearningLayer.split_data_balanced_labels(approx_webobj_sizes, simplified_traffic_labels, 0.50)
model_training_data, model_training_labels, model_test_data, model_test_labels = MachineLearningLayer.split_data_balanced_labels(histogram_sizes, simplified_traffic_labels, 0.50)

#Debug printing
print " === Training Set ==="
for i in range(0, len(model_training_data)):
	print "{}: {}".format(model_training_labels[i], model_training_data[i][0:10])
print ""

#Debug printing
print " === Testing Set ==="
for i in range(0, len(model_test_data)):
	print "{}: {}".format(model_test_labels[i], model_test_data[i][0:10])
print ""

#Create the machine-learning adversary model
adversary_model = MachineLearningLayer.make_decision_tree_model(model_training_data, model_training_labels, model_test_data, model_test_labels)

print adversary_model
print ""

#-----------------------------------------------------------------------

import ThreatModellingLayer

"""
Use the ThreatModellingLayer to determine how accurately an adversary
can predict a visited webpage. Please note that the generated
predictive model, adversary_model, at this point has already evaluated
itself against the provided testing data and labels.
"""

urls = ["https://en.wikipedia.org/wiki/Main_Page", "https://en.wikipedia.org/wiki/Toronto", "https://en.wikipedia.org/wiki/CN_Tower", "https://en.wikipedia.org/wiki/First_Canadian_Place", "https://en.wikipedia.org/wiki/PATH_(Toronto)"]
adv_performances = {}

for url in urls:
	adv_perf = ThreatModellingLayer.https.evaluate_page_loaded_prediction(adversary_model, url)
	adv_performances[url] = adv_perf
	print "\tAdversary Performance: {}".format(adv_perf)


#-----------------------------------------------------------------------

import ReactiveLayer

"""
Use the ReactiveLayer to render a webpage with guages showing the
machine learning modelled adversary's sucess at expoliting the
side-channel cues.
"""

#Create the object of the report webpage
report_webpage = ReactiveLayer.ReportWebpage()

for url in adv_performances:
	guage_name = "/img/Predict_URL_{}.png".format(ReactiveLayer.calculate_sha256(url))
	graph_title = ReactiveLayer.sanitize_url(url)
	ReactiveLayer.polar_guages.render_guage_image(0, 100, int(100*adv_performances[url]), "/www" + guage_name)
	
	#Add this information to the report webpage
	report_webpage.add_infocard("Adversary Score for Predicting {}".format(graph_title), guage_name)

#Render the HTML page
report_webpage.render_html("/www/index.html")
