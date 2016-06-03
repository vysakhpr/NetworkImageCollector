import threading
nme_ip="127.0.0.1"
nme_port=5005
no_of_nodes=0
event=threading.Event()
lock=threading.Lock()


class Nodes(object):
	"""The Motes or Entities in the Underlying RPL Network---Store the nodes according to rank"""

	def __init__(self,rank=0):
		super(Nodes, self).__init__()
		self.ip_address="127.0.0.1"
		self.battery=100
		self.packet_rate=0
		self.queue_length=0
		self.parent_links=[]
		self.parent_list=[]
		self.rank=rank
		
	def set_ip_address(self,arg):
		lock.acquire()
		self.ip_address=arg
		lock.release()

	def set_battery(self,arg):
		lock.acquire()
		self.battery=arg
		lock.release()

	def set_packet_rate(self,arg):
		lock.acquire()
		self.packet_rate =arg
		lock.release()

	def set_queue_length(self,arg):
		lock.acquire()
		self.queue_length=arg
		lock.release()

	def set_rank(self,arg):
		lock.acquire()
		self.rank=arg
		lock.release()

	def add_parent(self,ip,ss,per):
		lock.acquire()
		if ip in self.parent_list:
			lock.release()
			return
		self.parent_links.append(ParentLinks(ip,ss,per))
		self.parent_list.append(ip)
		lock.release()		

	def remove_parent(self,ip):
		lock.acquire()
		self.parent_list.remove(ip)
		lock.release()

	def get_ip_address(self):
		lock.acquire()
		temp=self.ip_address
		lock.release()
		return temp

	def get_battery(self):
		lock.acquire()
		temp=self.battery
		lock.release()
		return temp

	def get_packet_rate(self):
		lock.acquire()
		temp=self.packet_rate
		lock.release()
		return temp	

	def get_queue_length(self):
		lock.acquire()
		temp=self.queue_length
		lock.release()
		return temp

	def get_parent_links(self):
		lock.acquire()
		temp=self.parent_links
		lock.release()
		return temp

	def get_parent_list(self):
		lock.acquire()
		temp=self.parent_list
		lock.release()
		return temp

	def get_rank(self):
		lock.acquire()
		temp=self.rank
		lock.release()
		return temp




class ParentLinks(object):
	"""The Links eminating from a Node--Has IP, Signal Strength, Packet Error Ratio"""
	def __init__(self, ip,ss,per):
		super(ParentLinks, self).__init__()
		self.parent_ip=ip
		self.signal_strength=ss
		self.packet_error_rate=per
		

	def get_parent_ip(self):
		return self.parent_ip

	def get_signal_strength(self):
		return self.signal_strength

	def get_packet_error_rate(self):
		return self.packet_error_rate



def find_node(node_list, ip):
	global no_of_nodes
	#print no_of_nodes
	for i in range(no_of_nodes):
		if node_list[i].get_ip_address()==ip:
			return i
	return -1


def find_rank_of_ip(ip,node_list):
	source=node_list[find_node(node_list,ip)]
	return source.get_rank()

def display_network(node_list):
	for node in node_list:
		print "Node IP:",
		print node.get_ip_address()
		print "Rank:",
		print node.get_rank()
		print "Packet Data Rate:",
		print node.get_packet_rate()
		"""
		print "No of parents:",
		print len(node.get_parent_list())
		"""
		print "Parents:",
		for parent in node.get_parent_list():
			print parent+"\t",
		print ""
		print "=============================================="
		


def convert_neighbor_to_parent(graph_nodes):
	for node in graph_nodes:
		for parent_ip in node.get_parent_list():
			parent_rank=graph_nodes[find_node(graph_nodes,parent_ip)].get_rank()
			if parent_rank >= node.get_rank():
				node.remove_parent(parent_ip)
	return graph_nodes