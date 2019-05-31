#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import numpy as np
from matplotlib import pyplot as plt

def render_guage_image(min_val, max_val, read_val, filename):
	fig, ax = plt.subplots(subplot_kw=dict(polar=True))
	size = 0.3
	
	valsleft = np.array([[2*np.pi*(float(read_val)/float(max_val)), 2*np.pi], [0, 2*np.pi*(float(read_val)/float(max_val))]])
	widths = [2*np.pi*(1-((float(read_val)/float(max_val)))), 2*np.pi*(float(read_val)/float(max_val))]
	
	cmap = plt.get_cmap("coolwarm")
	outer_colors = cmap(np.arange(2)*500)
	
	#Draw it!
	#ax.bar(x=valsleft[:,0], width=widths, bottom=1-size, height=size, color=outer_colors, edgecolor='w', linewidth=1, align="edge")
	ax.bar(valsleft[:,0], [size, size], width=widths, bottom=1-size, color=outer_colors, edgecolor='w', linewidth=1, align="edge")
	ax.set_axis_off()
	
	#Put a textual representation of the value on the graph
	plt.text(0,0, "{}%".format(read_val), fontsize=36, horizontalalignment='center', verticalalignment='center')
	
	#Save the rendered image to a file
	plt.savefig(filename)


if __name__ == '__main__':
	#Test me!
	for i in range(0,101,10):
		render_guage_image(0, 100, i, "guage_{}.png".format(i))
