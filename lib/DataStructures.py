from __future__ import  division
import threading
event=threading.Event()
lock=threading.Lock()
graph_nodes=[]
no_of_nodes=6
udp_packets_received_from_network=0
initial_udp_packets=0
class Nodes(object):
	"""docstring for Nodes"""
	def __init__(self, ip, battery, packets,packetrate,timestamp,udppacketssent ,framessent, framesdropped,link_cost_to_parent, preferred_parent):
		super(Nodes, self).__init__()
		lock.acquire()
		self.ip = ip
		self.battery= battery
		self.udp_packets_sent=udppacketssent
		self.packets=packets
		self.packet_rate=packetrate
		self.timestamp=timestamp
		self.frames_sent=framessent
		self.frames_dropped=framesdropped
		self.link_cost_to_parent=link_cost_to_parent
		self.preferred_parent=preferred_parent
		self.parent_list=[]
		if framessent==0:
			self.packet_delivery_ratio=100
		else:
			self.packet_delivery_ratio=(int(framessent)/(int(framessent)+int(framesdropped)))*100
		lock.release()

	def update_node(self,ip,battery,packets,packetrate,timestamp,udppacketssent,framessent,framesdropped,link_cost_to_parent, preferred_parent):
		lock.acquire()
		self.ip = ip
		self.battery= battery
		self.udp_packets_sent=udppacketssent
		self.packets=packets
		self.packet_rate=packetrate
		self.timestamp=timestamp
		self.frames_sent=framessent
		self.frames_dropped=framesdropped
		self.link_cost_to_parent=link_cost_to_parent
		self.preferred_parent=preferred_parent
		self.parent_list=[]
		if framessent==0:
			self.packet_delivery_ratio=100
		else:
			self.packet_delivery_ratio=(int(framessent)/(int(framessent)+int(framesdropped)))*100		
		lock.release()

	def add_parent(self, ip, framessent, framesdropped):
		lock.acquire()
		self.parent_list.append(ParentStats(ip,framessent,framesdropped))
		lock.release()

	def update_parent(self, ip, framessent, framesdropped):
		lock.acquire()
		for parent in self.parent_list:
			if parent.get_ip()==ip:
				parent.ip = ip
				parent.frames_sent=framessent
				parent.frames_dropped=framesdropped
				if framessent==0:
					parent.packet_delivery_ratio=100
				else:
					parent.packet_delivery_ratio=(int(framessent)/(int(framessent)+int(framesdropped)))*100
				lock.release()
				return True
		lock.release()
		return False


	def get_udp_packets_sent(self):
		return self.udp_packets_sent

	def get_ip(self):
		return self.ip

	def get_packets(self):
		return self.packets

	def get_packet_rate(self):
		return self.packet_rate

	def get_timestamp(self):
		return self.timestamp

	def get_battery(self):
		return self.battery

	def get_frames_sent(self):
		return self.frames_sent

	def get_frames_dropped(self):
		return self.frames_dropped

	def get_pdr(self):
		return self.packet_delivery_ratio

	def get_link_cost_to_parent(self):
		return self.link_cost_to_parent

	def get_preferred_parent():
		return self.preferred_parent

	def get_parent_ip(self):
		ip=[]
		for parent in self.parent_list:
			ip.append(parent.get_ip())
		return ip

	def get_parent_stat_frames_sent(self,ip):
		for parent in parent_list:
			if parent.get_ip()==ip:
				return parent.get_frames_sent()
		return -1

	def get_parent_stat_frames_dropped(self,ip):
		for parent in parent_list:
			if parent.get_ip()==ip:
				return parent.get_frames_dropped()
		return -1

	def get_parent_stat_pdr(self,ip):
		for parent in parent_list:
			if parent.get_ip()==ip:
				return parent.get_pdr()
		return -1


class ParentStats(object):
	"""docstring for ParentStats"""
	def __init__(self, ip, framessent, framesdropped):
		super(ParentStats, self).__init__()
		self.ip = ip
		self.frames_sent=framessent
		self.frames_dropped=framesdropped
		if framessent==0:
			self.packet_delivery_ratio=100
		else:
			self.packet_delivery_ratio=(int(framessent)/(int(framessent)+int(framesdropped)))*100

	def get_ip(self):
		return self.ip

	def get_frames_sent(self):
		return self.frames_sent

	def get_frames_dropped(self):
		return self.frames_dropped

	def get_pdr(self):
		return self.packet_delivery_ratio

def find_node_index(ip):
	for node in graph_nodes:
		if node.get_ip()==ip:
			return graph_nodes.index(node)
	return -1


def format_ip(ip):
	ip_sections=ip.split(':')
	ip=""
	#print ip_sections
	for section in ip_sections:
		if section=="0000":
			ip=ip+"0:"
		else:
			i=0
			while(section[i]=="0"):
				i=i+1
			ip=ip+section[i:]+":"
	return ip[:-1]	
