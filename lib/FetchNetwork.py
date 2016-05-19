import  lib.DataStructures
import socket

from coapthon.client.coap import CoAP
from coapthon.client.helperclient import HelperClient
from coapthon.messages.message import Message
from coapthon.messages.request import Request


        
def init(graph_nodes):
	ip_addresses=[line.rstrip('\n') for line in open('lib/addresses')]
	try:
		for ip in ip_addresses:			
			host,port=parse_ipv6_uri(ip)
			parent_ip=[]
			client = HelperClient(server=(host, port))
			node_details_response=client.get("Get-Packet-Rate")
			contents=node_details_response.payload.split(";")
			source=node_details_response.source[0]
			source=source.split("::")[1]
			#source=":".join(groups[4:])
			source=format_suffix(source)
			rank=contents[0]
			no_of_parents=contents[1]
			packet_rate=contents[2].strip()
			#client.stop()
			#client = HelperClient(server=(host, port))
			parent_details_response=client.get("Get-Parent")
			parents=parent_details_response.payload.split(";")
			print parents
			for parent in parents:
				if parent.strip()!="":
					parent_ip.append(parent.strip())
			print parent_ip
			client.stop()
			
			"""	
			node_index=lib.DataStructures.find_node(graph_nodes,source)
			if node_index==-1:
				graph_nodes.append(lib.DataStructures.Nodes())
				graph_nodes[lib.DataStructures.no_of_nodes].set_ip_address(source)
				graph_nodes[lib.DataStructures.no_of_nodes].set_packet_rate(packet_rate)
				graph_nodes[lib.DataStructures.no_of_nodes].set_rank(rank)
				for parent in parent_ip:
					graph_nodes[lib.DataStructures.no_of_nodes].add_parent(parent,0,1)
				lib.DataStructures.no_of_nodes=lib.DataStructures.no_of_nodes+1
			else:
				graph_nodes[node_index].set_packet_rate(packet_rate)
				graph_nodes[node_index].set_rank(rank)
				for parent in parent_ip:
					graph_nodes[node_index].add_parent(parent,0,1)
			lib.DataStructures.display_network(graph_nodes)
			"""

	except socket.error :
			print "Cannot connect to RPL Network"
			client.stop()
			print "Client Shutdown"
	except KeyboardInterrupt:
			print "Communication Disrupted by client"
			client.stop()
			print "Client Shutdown"
		




def parse_ipv6_uri(ipv6_address):
	(ip,port)=ipv6_address.rsplit(':',1)
	port=int(port)
	ip=ip.replace('[','')
	ip=ip.replace(']','')
	return(ip,port)


def format_suffix(suffix):
	sub_parts=suffix.split(":")
	formatted_suffix=""
	for part in sub_parts:
		for i in range(4-len(part)):
			part="0"+part
		formatted_suffix=formatted_suffix+part+":"
	return formatted_suffix[:-1]