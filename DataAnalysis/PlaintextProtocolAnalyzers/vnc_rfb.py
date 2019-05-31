#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Contains methods for extracting event data from streams of data using
the Virtual Network Computing Remote FrameBuffer Protocol.
"""

def key_event_tagger(prev_state, tcp_payload):
	new_state = ['NULL', '']
	if len(tcp_payload) == 8:
		if ord(str(tcp_payload)[0]) == 4:
			if ord(str(tcp_payload)[7]) in range(33, 127):
				#This is a KeyEvent packet
				key_updown = ord(str(tcp_payload)[1])
				ascii_key = str(tcp_payload)[7]
				if key_updown == 1:
					#Key pressed down
					new_state = ['PRESS', ascii_key]
				
				elif key_updown == 0:
					#Key released
					new_state = ['RELEASE', ascii_key]
	
	if new_state[0] == 'PRESS':
		return new_state[:]
	
	if new_state[0] == 'NULL':
		if prev_state == None:
			return None
		elif type(prev_state) == list:
			if prev_state[0] == 'PRESS':
				return prev_state[:]
	
	if new_state[0] == 'RELEASE':
		return None
