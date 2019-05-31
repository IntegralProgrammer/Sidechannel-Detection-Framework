#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import matplotlib
matplotlib.use('Agg')

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches 

def render_entropy_target(maximum_entropy, measured_entropy, title, filename):
	fig, ax = plt.subplots(1)
	#ax.set_ylim(0,1.5)
	#ax.set_xlim(0,1.5)
	
	rect1 = patches.Rectangle((0,0), 1.0, 1.0, color='r',  label='Maximum Entropy: {} bits'.format(maximum_entropy))
	ax.add_patch(rect1)
	
	percent_entropy = float(measured_entropy) / float(maximum_entropy)
	sidelength = math.sqrt(percent_entropy)
	rect2 = patches.Rectangle(((1.0 - sidelength) / 2, (1.0 - sidelength) / 2), sidelength, sidelength, color='g', label='Measured Entropy: {} bits'.format(measured_entropy))
	ax.add_patch(rect2)
	
	rect3 = patches.Rectangle((0, 1.0), 2.0, 2.0, color='w')
	ax.add_patch(rect3)
	
	ax.legend(framealpha=1.0)
	plt.axis('off')
	
	#plt.text(0, 1.1, 'Measured Entropy: {} bits'.format(measured_entropy), size=20, color='g')
	#plt.text(0, 1.3, 'Maximum Entropy: {} bits'.format(maximum_entropy), size=20, color='r')
	plt.title(title, fontsize=25)
	
	#Save the rendered image to a file
	plt.savefig(filename)

if __name__ == '__main__':
	#Test me!
	render_entropy_target(100, 50, "Password Entropy", "entropy_test.png")
