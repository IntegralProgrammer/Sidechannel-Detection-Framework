#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../../')

#-----------------------------------------------------------------------

"""
In the Data Gathering Layer, we will simply open the halt logging file
and create a 'labels' list and a 'data' list.
"""

CPU_INSTRUMENTATION_LOGFILE = "filtered_halts.log"
PASSWORD_CORRECTNESS_ATTEMPTS = []
for i in range(4):
	for j in [0,10,20,30,40,50,60,70,80,90,100]:
		PASSWORD_CORRECTNESS_ATTEMPTS.append(j)


cpu_inst_labels = []
cpu_inst_data = []

f_cpuinst = open(CPU_INSTRUMENTATION_LOGFILE, 'r')

line = f_cpuinst.readline()
cursor_x = 0
while True:
	if not line:
		break
	
	if line == "\n":
		break
	
	inst_count = int(line.rstrip())
	if inst_count == -1:
		#There was an issue with the logging process, skip this sample.
		line = f_cpuinst.readline()
		cursor_x += 1
		continue
	
	cpu_inst_labels.append(PASSWORD_CORRECTNESS_ATTEMPTS[cursor_x])
	cpu_inst_data.append([inst_count])
	
	cursor_x += 1
	line = f_cpuinst.readline()

f_cpuinst.close()

#-----------------------------------------------------------------------

"""
Feature Extraction Layer: Nothing to be done here. Feature Extraction
was done in real-time in the Bochs instrumentation file.
"""

#-----------------------------------------------------------------------

import MachineLearningLayer

#Split data
model_training_data, model_training_labels, model_test_data, model_test_labels = MachineLearningLayer.split_data_balanced_labels(cpu_inst_data, cpu_inst_labels, 0.50)

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

"""
In the Threat Modelling Layer we will measure the expected amount of
trials to crack the password under the given side-channels.
"""

measured_entropy = ThreatModellingLayer.string_compare.calculate_string_entropy(adversary_model, 10, 1000)

#-----------------------------------------------------------------------

import ReactiveLayer
import math

"""
In the Reactive Layer we will render an image depicting the 'true'
entropy of the password entry.
"""

max_pw_entropy = math.log(10 ** 1000 ,2)

print "The password has an estimated {} bits of entropy.".format(measured_entropy)
print "Without side-channels, the password would have {} bits of entropy.".format(max_pw_entropy)

#Render!
ReactiveLayer.entropy_target.render_entropy_target(max_pw_entropy, measured_entropy, "Entry Code True Entropy", "/www/passcode_entropy.png")
