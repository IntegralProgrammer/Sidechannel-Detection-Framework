#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import socket
import json
import time

UDP_IP = '172.19.0.3'
UDP_PORT = 5006
UDP_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def callback_begin_command(command, context, timestamp):
	infogram = {"state": "begin", "command": command, "context": context, "timestamp": timestamp}
	UDP_SOCK.sendto(json.dumps(infogram), (UDP_IP, UDP_PORT))

def callback_end_command(command, context, timestamp):
	infogram = {"state": "end", "command": command, "context": context, "timestamp": timestamp}
	UDP_SOCK.sendto(json.dumps(infogram), (UDP_IP, UDP_PORT))

print "=== UDP Logging Shell Started ==="
print ""
print ""

stillRunning = False

while True:
	working_dir = os.path.abspath('.')
	home_dir = os.path.expanduser('~')
	rel_dir = os.path.relpath(working_dir, start=home_dir)
	if len(rel_dir) >= 2:
		if rel_dir[0:2] == '..':
			resolved_dir = working_dir
		else:
			if rel_dir == '.':
				rel_dir = ''
			resolved_dir = "~" + rel_dir
	else:
		if rel_dir =='.':
			rel_dir = ''
		resolved_dir = "~" + rel_dir
	
	sys.stdout.write("ubuntu@ubuntu:{}$ ".format(resolved_dir))
	sys.stdout.flush()
	#Command call ends here
	if stillRunning:
		#time.sleep(0.250)
		callback_end_command(old_cmd, old_working_dir, old_call_timestamp)
		stillRunning = False
	
	cmd = raw_input("")
	if cmd == "exit":
		break
	
	if len(cmd) >= 4:
		if cmd[0:3] == "cd ":
			path_change = cmd[3:]
			if cmd[3] == '~':
				path_change = home_dir
			
			call_timestamp = time.time()
			callback_begin_command(cmd, working_dir, call_timestamp)
			os.chdir(path_change)
			#callback_end_command(cmd, working_dir, call_timestamp)
			old_cmd = cmd
			old_working_dir = working_dir
			old_call_timestamp = call_timestamp
			stillRunning = True
			continue
	
	#print "BEGIN {} in context of {}".format(cmd, working_dir)
	call_timestamp = time.time()
	callback_begin_command(cmd, working_dir, call_timestamp)
	#time.sleep(0.250)
	os.system(cmd)
	old_cmd = cmd
	old_working_dir = working_dir
	old_call_timestamp = call_timestamp
	stillRunning = True
	#callback_end_command(cmd, working_dir, call_timestamp)
	#print "END {} in context of {}".format(cmd, working_dir)
