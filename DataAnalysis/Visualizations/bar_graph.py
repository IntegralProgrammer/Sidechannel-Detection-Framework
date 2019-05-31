#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import matplotlib as mpl

def get_bar_color(value, min_val, max_val):
	rgba = cm.jet(float(value - min_val) / float(max_val - min_val))
	return rgba

def render_bar_graph(min_val, max_val, categories, values, xlabel, ylabel, filename, linewidth=None):
	fig, ax = plt.subplots(1)
	ax.set_xlim(0, len(values) + 1)
	
	all_x = np.array(range(len(values))) + 1.0
	
	ax.set_xticks(all_x + 0.5)
	ax.set_xticklabels(categories)
	
	colors = cm.jet(values)
	plot = plt.scatter(values, values, c=values, cmap='jet')
	plt.clf()
	plt.colorbar(plot)
	
	for i in range(len(values)):
		if linewidth is None:
			plt.bar(all_x[i], values[i], color=get_bar_color(values[i], min_val, max_val))
		else:
			plt.bar(all_x[i], values[i], color=get_bar_color(values[i], min_val, max_val), linewidth=linewidth)
	
	#if linewidth is None:
	#	plt.bar(np.array(range(len(categories))) + 1.00, values, color=colors)
	#else:
	#	plt.bar(np.array(range(len(categories))) + 1.00, values, color=colors, linewidth=linewidth)
	
	
	#cbar = ax.figure.colorbar(orientation='vertical')
	#mpl.colorbar.ColorbarBase(ax, cmap=cm.jet, norm=mpl.colors.Normalize(vmin=min_val, vmax=max_val), orientation='vertical')
	
	plt.gca().set_xticks(all_x + 0.5)
	plt.gca().set_xticklabels(categories)
	
	#Save the rendered image to a file
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.savefig(filename)

if __name__ == '__main__':
	#Test me!
	alphabet = []
	test_vals = []
	for k in 'abcdefghijklmnopqrstuvwxyz':
		alphabet.append(k)
		test_vals.append(ord(k))
	
	render_bar_graph(95, 120, alphabet, test_vals, 'bar_graph_test.png')
