from __future__ import division
import lib.DataStructures
import os
import rrdtool
import time
def init(lock):
	hosts=[]
	i=2
	statement='ret = rrdtool.create("lib/rrd/packet_rate.rrd", "--step", "15", "--start", "0",'
	while i<=lib.DataStructures.no_of_nodes:
		#hosts.append("aaaa::200:0:0:"+str(i))
		datasource_string='"DS:%(host)s:GAUGE:120:U:U",' %{'host':"NodeId-"+str(i)}
		statement=statement+datasource_string
		i=i+1
	statement=statement+'"RRA:AVERAGE:0.5:1:5760","RRA:MAX:0.5:1:5760")'
	exec statement


	ret = rrdtool.create("lib/rrd/packet_delivery_rate.rrd", "--step", "15", "--start", "0",
		"DS:pdr:GAUGE:120:U:U",
		"RRA:AVERAGE:0.5:1:5760",
		"RRA:MAX:0.5:1:5760")
	time.sleep(15)


	while True:
		print("RRD Listening and Updating")
		lock.acquire()
		statement='ret = rrdtool.update("lib/rrd/packet_rate.rrd","N:'
		i=2
		while i<=lib.DataStructures.no_of_nodes:
			if lib.DataStructures.find_node_index("aaaa::200:0:0:"+str(i))==-1:
				continue
			packet_sent=lib.DataStructures.graph_nodes[lib.DataStructures.find_node_index("aaaa::200:0:0:"+str(i))].get_packet_rate()
			if i==lib.DataStructures.no_of_nodes:
				statement=statement+str(packet_sent)+'"'
			else:
				statement=statement+str(packet_sent)+":"
			i=i+1
		statement=statement+')'
		exec statement
		pdr=0
		total_udp_packets_received=lib.DataStructures.udp_packets_received_from_network
		total_udp_packets_sent=0
		for node in lib.DataStructures.graph_nodes:
			total_udp_packets_sent=total_udp_packets_sent+node.get_udp_packets_sent()
		if total_udp_packets_sent!=0:
			pdr=(total_udp_packets_received/total_udp_packets_sent)*100
			pdr=round(pdr,1)
			pdr=str(pdr)
		ret = rrdtool.update("lib/rrd/packet_delivery_rate.rrd","N:%s" % pdr )
		lock.release()
		time.sleep(15)
		#ret = rrdtool.update('lib/rrd/node.rrd', 'N:%s:%s' %(FramesSent, FramesDropped));
		#time.sleep(15)