#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *
import json

"""
Parses the file defined by (pcap_file). UDP datagrams on the specified
port (tag_udpport) specify the beginnings and ends of relevant sequences
of TCP datagrams for a given event.

UDP datagram should be carrying JSON datagram containing at least the
(timestamp) and (state) fields.
"""
def get_pcap_labeled_sequences(pcap_file, tag_udpport, datastream_tcpport):
	relevant_packets = []
	data_labels = []
	data_profiles = []
	current_timestamp = None
	packet_capture = rdpcap(pcap_file)
	for pkt in packet_capture:
		if pkt.haslayer(UDP):
			if pkt[UDP].dport == tag_udpport:
				"""
				Is this a packet which tags the beginning of a response?
				"""
				try:
					udp_label = json.loads(str(pkt[UDP].payload))
				except:
					continue
				
				"""
				Is it a valid UDP tag?
				"""
				if type(udp_label) != dict:
					continue
				
				if 'timestamp' not in udp_label:
					continue
				
				if 'state' not in udp_label:
					continue
				
				
				if udp_label['state'] == 'begin':
					current_timestamp = udp_label['timestamp']
					relevant_packets = []
				
				if udp_label['state'] == 'end' and udp_label['timestamp'] == current_timestamp:
					"""
					Save all relevant_packets to data_profiles and
					label appropriately.
					"""
					data_profiles.append(relevant_packets[:])
					relevant_packets = []
					data_labels.append(udp_label.copy())
		
		if pkt.haslayer(TCP):
			if pkt[TCP].sport == datastream_tcpport:
				relevant_packets.append(len(pkt[TCP].payload))
	
	return data_labels, data_profiles

"""
Parses the file defined by (pcap_file). Extracts the datastream of
packets moving from plain_src=(plain_src_ip, plain_src_port) to
plain_dst=(plain_dst_ip, plain_dst_port) and adds tags based on the
passed method plaintext_tagger to the encrypted version of the
datastream moving from crypto_src=(crypto_src_ip, crypto_src_port) to
crypto_dst=(crypto_dst_ip, crypto_dst_ip).
"""
def get_pcap_ssh_encrypted_sequence(pcap_file, plain_src, plain_dst, crypto_src, crypto_dst, plaintext_tagger):
	plain_src_ip = plain_src[0]
	plain_src_port = plain_src[1]
	plain_dst_ip = plain_dst[0]
	plain_dst_port = plain_dst[1]
	crypto_src_ip = crypto_src[0]
	crypto_src_port = crypto_src[1]
	crypto_dst_ip = crypto_dst[0]
	crypto_dst_port = crypto_dst[1]
	packet_capture = rdpcap(pcap_file)
	label_state = None
	last_label_state = None
	relevant_packets = []
	for pkt in packet_capture:
		if pkt.haslayer(TCP):
			#Plain_SRC --> Plain_DST
			if pkt[IP].src == plain_src_ip and pkt[IP].dst == plain_dst_ip and (pkt[TCP].sport == plain_src_port or plain_src_port == "*") and (pkt[TCP].dport == plain_dst_port or plain_dst_port == "*"):
				#Call plaintext tagger on this TCP payload
				label_state = plaintext_tagger(label_state, pkt[TCP].payload)
				#print "Label State is now {}".format(label_state)
			
			#Crypto_SRC --> Crypto_DST
			if pkt[IP].src == crypto_src_ip and pkt[IP].dst == crypto_dst_ip and (pkt[TCP].sport == crypto_src_port or crypto_src_port == "*") and (pkt[TCP].dport == crypto_dst_port or crypto_src_port == "*"):
				if label_state is not None:
					#This encrypted packet belongs to the tagged event
					relevant_packets.append(len(pkt[TCP].payload))
					last_label_state = label_state
					#print "Found a relevant packet of {} bytes".format(len(pkt[TCP].payload))
				else:
					if len(relevant_packets) > 0 and last_label_state is not None:
						#We have captured some encrypted packets corresponding to the plaintext event of interest
						evt = last_label_state
						last_label_state = None
						this_relevant_packets = relevant_packets[:]
						relevant_packets = []
						yield (evt, this_relevant_packets[:])
	


"""
Checks each object in llist and, for each, returns a simplified object
containg only the key-value pairs for which the keys can be found in
keeplist.
"""
def filter_labels_list(llist, keeplist):
	for obj in llist:
		simp_obj = {}
		for key in keeplist:
			if key in obj:
				simp_obj[key] = obj[key]
		yield simp_obj


"""
Iterates through a 1D array of frame/packet/payload sizes (stream) and
yields the sizes of these bursts of N-sized entities
"""
def NBurst_detector(stream, n):
	running_counter = 0
	for itm in stream:
		if itm == n:
			running_counter += n
		else:
			if running_counter == 0:
				continue
			else:
				yield running_counter + itm
				running_counter = 0

"""
Iterates through a stream of packets and for all packets that are
matched by filter_method() if they have a time spacing of 'spacing'
subject to a tolerance of 'tolerance' - they are yielded. This generator
method is useful for analyzing packet streams associated with real-time
systems such as VoIP traffic.
"""
def packet_timing_density_detector(pcap_file, filter_method, spacing, tolerance):
	stream = rdpcap(pcap_file)
	prev_pkt_time = None
	this_cluster = []
	for pkt in stream:
		if not filter_method(pkt):
			continue
		
		if prev_pkt_time is None:
			prev_pkt_time = pkt.time
			continue
		
		#Does this packet fall within the tolerance of the time spacing?
		min_timebound = spacing - spacing*tolerance
		max_timebound = spacing + spacing*tolerance
		time_diff = pkt.time - prev_pkt_time
		if time_diff >= min_timebound and time_diff <= max_timebound:
			this_cluster.append(pkt)
		else:
			#Check if we have just left a cluster
			if len(this_cluster) != 0:
				yield this_cluster[:]
				this_cluster = []
		
		prev_pkt_time = pkt.time


def get_label_times(pcap_file, udp_port):
	stream = rdpcap(pcap_file)
	for pkt in stream:
		if pkt.haslayer(UDP):
			if pkt[UDP].dport == udp_port:
				#Read the payload of this packet
				udp_label = json.loads(str(pkt[UDP].payload))
				yield (pkt.time, udp_label)


def labels_to_spans(labels):
	for lbl in labels:
		if lbl[1]['state'] == 'begin':
			this_ts = lbl[1]['timestamp']
			#Find the matching 'end' label
			for elbl in labels:
				if elbl[1]['state'] == 'end' and elbl[1]['timestamp'] == this_ts and elbl[0] > lbl[0]:
					yield (lbl[0], elbl[0], lbl[1])
					break


def label_cluster(ti, tf, spans):
	#Get spans
	#spans = list(labels_to_spans(labels))
	for sp in spans:
		if sp[0] < ti and sp[1] > tf:
			yield sp[2]


