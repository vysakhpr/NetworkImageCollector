nme_ip="127.0.0.1"
nme_port=5005
no_of_nodes=0


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
		self.ip_address=arg

	def set_battery(self,arg):
		self.battery=arg

	def set_packet_rate(self,arg):
		self.packet_rate =arg

	def set_queue_length(self,arg):
		self.queue_length=arg

	def set_rank(self,arg):
		self.rank=arg

	def add_parent(self,ip,ss,per):
		self.parent_links.append(ParentLinks(ip,ss,per))
		self.parent_list.append(ip)		

	def get_ip_address(self):
		return self.ip_address

	def get_battery(self):
		return self.battery

	def get_packet_rate(self):
		return self.packet_rate

	def get_queue_length(self):
		return self.queue_length

	def get_parent_links(self):
		return self.parent_links

	def get_parent_list(self):
		return self.parent_list

	def get_rank(self):
		return self.rank




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
		print "Parents:",
		for parent in node.get_parent_list():
			print parent+"\t",


