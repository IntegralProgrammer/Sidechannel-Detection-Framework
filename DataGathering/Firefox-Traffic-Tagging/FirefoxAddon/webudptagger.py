#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import sys
import struct
import hashlib

UDP_IP = '172.17.0.1' #Send to docker0 interface
UDP_PORT = 5005
UDP_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Read and decode a message from Firefox addon
def get_message():
	raw_length = sys.stdin.read(4)
	if not raw_length:
		sys.exit(0)
	message_length = struct.unpack('=I', raw_length)[0]
	message = sys.stdin.read(message_length)
	return json.loads(message)

#Encode a message for Firefox addon
def encode_message(message_content):
	encoded_content = json.dumps(message_content)
	encoded_length = struct.pack('=I', len(encoded_content))
	return {'length': encoded_length, 'content': encoded_content}

#Send an encoded message to the Firefox addon
def send_message(encoded_message):
	sys.stdout.write(encoded_message['length'])
	sys.stdout.write(encoded_message['content'])
	sys.stdout.flush()

"""
When the Firefox addon sends a message about a web browsing event,
tag the traffic.
"""
while True:
	message = get_message()
	#UDP_SOCK.sendto("BrowserEvent", (UDP_IP, UDP_PORT))
	#UDP_SOCK.sendto(message, (UDP_IP, UDP_PORT))
	detailed_message = {}
	detailed_message['state'] = json.loads(message)['state']
	detailed_message['url'] = json.loads(message)['url']
	hasher = hashlib.sha256()
	hasher.update('<windowId>')
	hasher.update(str(json.loads(message)['windowId']))
	hasher.update('</windowId>')
	hasher.update('<tabId>')
	hasher.update(str(json.loads(message)['tabId']))
	hasher.update('</tabId>')
	detailed_message['timestamp'] = hasher.hexdigest()
	UDP_SOCK.sendto(json.dumps(detailed_message), (UDP_IP, UDP_PORT))
