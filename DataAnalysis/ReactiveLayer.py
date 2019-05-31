#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../../Visualizations')

import hashlib

import polar_guages
import bar_graph
import entropy_target

HTML_REPORT_HEADER_FILE = "../../Visualizations/html_report_header.html"
HTML_REPORT_FOOTER_FILE = "../../Visualizations/html_report_footer.html"

class ReportWebpage:
	def __init__(self):
		self.infocards = []
	
	def add_infocard(self, title, graph_img):
		self.infocards.append((title, graph_img))
	
	def render_begin_row(self):
		return '<div class="row">\n'
	
	def render_end_row(self):
		return '</div>\n'
	
	def render_begin_col(self):
		return '<div class="col-sm-4">\n'
	
	def render_end_col(self):
		return '</div>\n'
	
	def render_html(self, output_file):
		f_html = open(output_file, 'w')
		
		#Add the page header
		f_header = open(HTML_REPORT_HEADER_FILE, 'r')
		f_html.write(f_header.read())
		f_header.close()
		
		for i in range(0, len(self.infocards)):
			title = self.infocards[i][0]
			img_url = self.infocards[i][1]
			
			if (i % 3 == 0 and i != 0):
				f_html.write(self.render_end_row())
			
			#Should a new row be created?
			if i % 3 == 0:
				f_html.write(self.render_begin_row())
			
			
			f_html.write(self.render_begin_col())
			f_html.write('<div class="card" style="width: 18rem;">\n')
			f_html.write('\t<img class="card-img-top" src="{}" alt="Graph Here">\n'.format(img_url))
			f_html.write('\t<div class="card-body">\n')
			f_html.write('\t\t<p class="card-text">\n')
			f_html.write('\t\t\t{}\n'.format(title))
			f_html.write('\t\t</p>\n')
			f_html.write('\t</div>\n')
			f_html.write('</div>\n')
			f_html.write(self.render_end_col())
			
			#Are we about to exit? If so close up this row.
			if (i + 1) == len(self.infocards):
				f_html.write(self.render_end_row())
		
		#Add the page footer
		f_footer = open(HTML_REPORT_FOOTER_FILE, 'r')
		f_html.write(f_footer.read())
		f_footer.close()
		
		f_html.close()

def simple_log_warning(warn_msg, model_thresh, adversary_score):
	if adversary_score > model_thresh:
		print ""
		print "########### WARNING ###########"
		print ""
		print "\t{} (Adversary Score: {})".format(warn_msg, adversary_score)
		print ""
		print "###############################"
		print ""

def calculate_sha256(name_string):
	h = hashlib.sha256()
	h.update(name_string)
	return h.hexdigest()

def sanitize_url(web_url):
	alpha_lower = "abcdefghijklmnopqrstuvwxyz"
	alpha_upper = alpha_lower.upper()
	numbers = "1234567890"
	punctuation = "-_?.=+():/"
	ALLOWED_CHARS = alpha_lower + alpha_upper + numbers + punctuation
	clean_url = ""
	w_url = str(web_url)
	for c in w_url:
		if c in ALLOWED_CHARS:
			clean_url += c
	
	return clean_url
