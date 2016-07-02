from __future__ import division

import lib.DataStructures
from lib.coapthon.client.coap import CoAP
from lib.coapthon.client.helperclient import HelperClient
from lib.coapthon.messages.message import Message
from lib.coapthon.messages.request import Request
import calendar
import time

lib.DataStructures.graph_nodes=[]
def init():
	print "Starting Fetch Network Thread"
	prefix = "aaaa::200:0:0:"
	parents=[]
	port = 5684
	no_of_nodes=lib.DataStructures.no_of_nodes
	router = HelperClient(server = ("aaaa::200:0:0:1", 5684))
	response = router.get("Get-UDP-Packets-Received")
	router.stop()
	if response!=None: 
		if response.payload!=None:
			lib.DataStructures.udp_packets_received_from_network=int(response.payload)
			print"\n------------------------------------------------------------------------------------------------------------------------------------------------------	"
			print"\n------------------------------------------------------------------------------------------------------------------------------------------------------	"
			print "Total UDP Packets Received From Network:\t\t\t"+str(lib.DataStructures.udp_packets_received_from_network)+"\n"
	i=2
	while(True):
		host = prefix + str(i)
		ip=host
		print"\n------------------------------------------------------------------------------------------------------------------------------------------------------	"
		client = HelperClient(server = (host, port))
		response = client.get("Get-Packet-Rate")
		client.stop()
		if response==None:
			i=i+1
			if(i==no_of_nodes+1):
				i=2
				print "\nQueried All Nodes\n\n\n"
				break
			continue 
		if response.payload==None:
			i=i+1
			if(i==no_of_nodes+1):
				i=2
				print "\nQueried All Nodes\n\n\n"
				break
			continue 
		contents=response.payload.split(";")
		packets=int(contents[2].strip())
		udp_packets=0
		client = HelperClient(server = (host, port))
		response = client.get("Get-UDP-Packets")
		client.stop()

		if response!=None:
			if response.payload!=None: 
				udp_packets=int(response.payload)
		flag=0
		packet_rate=0
		for node in lib.DataStructures.graph_nodes:
			if node.get_ip()==ip:
				previous_packets=node.get_packets()
				previous_timestamp=node.get_timestamp()
				current_packets=int(packets)
				current_timestamp=calendar.timegm(time.gmtime())
				packet_rate=((current_packets-previous_packets)/(current_timestamp-previous_timestamp))
				packet_rate=round(packet_rate,4)
				#Impulsive Racket Rate
				#node.update_node(ip,0,packets,packet_rate,current_timestamp,0,0,1,"")
				#Average Packet Rate
				node.update_node(ip,0,previous_packets,packet_rate,previous_timestamp,udp_packets,0,0,1,"")
				flag=1
				break
		if flag==0:
			node=lib.DataStructures.Nodes(ip,packets,0,0,calendar.timegm(time.gmtime()),udp_packets,0,0,1,"")
			lib.DataStructures.graph_nodes.append(node)
		print"\nQuerying Node id \t:"+str(i)+"\tPackets Sent:\t"+str(packets)+"\tPacket Rate:\t"+str(packet_rate)+"\tUDP Packets:\t"+str(udp_packets)+"\n"
		i=i+1
		if(i==no_of_nodes+1):
			i=2
			print "\nQueried All Nodes\n\n\n"
			break



"""
client = HelperClient(server = (host, port))
		response = client.get("node/battery")
		client.stop()
		output=output+"BATTERY\t\t\t\t\t:"+str(response.payload)+"\n"
		battery=int(response.payload)
		client = HelperClient(server = (host, port))
		response = client.get("node/all_frames_sent")
		client.stop()
		fs=int(response.payload)
		output=output+"TOTAL FRAMES SENT SUCCESSFULLY\t\t:"+str(response.payload)+"\n"
		framessent=int(response.payload)
		client = HelperClient(server = (host, port))
		response = client.get("node/all_frames_dropped")
		client.stop()
		output=output+"TOTAL FRAMES DROPPED\t\t\t:"+str(response.payload)+"\n"
		framesdropped=int(response.payload)
		fd=int(response.payload)
		if fs!=0:
			pdr=(fs/(fs+fd))*100
		else:
			pdr=100.0
		output=output+"TOTAL PACKET DELIVERY RATIO\t\t:"+str(pdr)+"\n"
		client = HelperClient(server = (host, port))
		response = client.get("node/link_cost_with_parent")
		client.stop()
		output=output+"LINK COST\t\t\t\t:"+str(response.payload)+"\n"
		link_cost_to_parent=int(response.payload)
		client = HelperClient(server = (host, port))
		response = client.get("node/my_parent")
		client.stop()
		output=output+"PREFERRED PARENT IP\t\t\t:"+str(response.payload)+"\n"
		preferred_parent=str(response.payload)
		flag=0
		for node in lib.DataStructures.graph_nodes:
			if node.get_ip()==ip:
				node.update_node(ip,battery,framessent,framesdropped,link_cost_to_parent, preferred_parent)
				flag=1
				break
		if flag==0:
			node=lib.DataStructures.Nodes(ip,battery, framessent, framesdropped,link_cost_to_parent, preferred_parent)
			lib.DataStructures.graph_nodes.append(node)


		output=output+"STATISTICS PER PARENT\n\n"
		output=output+"\t\tPARENT IP\t\t\tFRAMES SENT SUCCESSFULLY\tFRAMES DROPPED\t\tPACKET DELIVERY RATIO\n"
		client = HelperClient(server = (host, port))
		response = client.get("Get-Parent")
		client.stop()
		parents=response.payload.split(';')
		for parent in parents[:-1]:
			output=output+"\t\t"+str(parent)+"\t\t\t"
			client = HelperClient(server = (host, port))
			response = client.post("node/frames_sent_per_parent","fe80::"+str(parent))
			fs=int(response.payload)
			client.stop()
			output=output+str(response.payload)+"\t\t\t\t"
			client = HelperClient(server = (host, port))
			response = client.post("node/frames_dropped_per_parent","fe80::"+str(parent))
			fd=int(response.payload)
			client.stop()
			if fs!=0:
				pdr=(fs/(fs+fd))*100
			else:
				pdr=100.0
			output=output+str(response.payload)+"\t\t"+str(pdr)+"%\n"

			for node in lib.DataStructures.graph_nodes:
				if node.get_ip()==ip:	
					if node.update_parent("aaaa::"+lib.DataStructures.format_ip(parent),fs,fd)==False:
						node.add_parent("aaaa::"+lib.DataStructures.format_ip(parent),fs,fd)
					break
		output=output+"------------------------------------------------------------------------------------------------------------------------------------------------------"
		statistics=statistics+output
"""