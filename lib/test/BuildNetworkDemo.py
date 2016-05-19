import lib.DataStructures


def initDemoOne():
	lib.DataStructures.no_of_nodes=0
	node_list=[]
	for i in range(5):
		node=lib.DataStructures.Nodes(i)
		node.set_ip_address("127.0.0."+str(i+1))
		node_list.append(node)
		lib.DataStructures.no_of_nodes=lib.DataStructures.no_of_nodes+1
	node_list[4].add_parent("127.0.0.2",-20,0)
	node_list[4].add_parent("127.0.0.3",-55,0)
	node_list[4].add_parent("127.0.0.4",-40,0)
	node_list[1].add_parent("127.0.0.1",-70,0)
	node_list[2].add_parent("127.0.0.1",-65,0)
	node_list[3].add_parent("127.0.0.1",-60,0)

	node_list[0].set_packet_rate(2)
	node_list[1].set_packet_rate(4)
	node_list[2].set_packet_rate(7)
	node_list[3].set_packet_rate(3)
	node_list[4].set_packet_rate(2)
	return node_list


def initDemoTwo():
	lib.DataStructures.no_of_nodes=0
	node_list=[]
	for i in range(13):
		node=lib.DataStructures.Nodes()
		node.set_ip_address("127.0.0."+str(i+1))
		node_list.append(node)
		lib.DataStructures.no_of_nodes=lib.DataStructures.no_of_nodes+1
	node_list[1].add_parent("127.0.0.1",-20,0)
	node_list[2].add_parent("127.0.0.1",-40,0)
	node_list[3].add_parent("127.0.0.2",-30,0)
	node_list[4].add_parent("127.0.0.2",-30,0)
	node_list[5].add_parent("127.0.0.5",-30,0)
	node_list[6].add_parent("127.0.0.5",-20,0)
	node_list[6].add_parent("127.0.0.4",-20,0)
	node_list[7].add_parent("127.0.0.4",-30,0)
	node_list[8].add_parent("127.0.0.1",-70,0)
	node_list[8].add_parent("127.0.0.3",-40,0)
	node_list[9].add_parent("127.0.0.6",-30,0)
	node_list[9].add_parent("127.0.0.7",-20,0)
	node_list[10].add_parent("127.0.0.4",-50,0)
	node_list[10].add_parent("127.0.0.8",-20,0)
	node_list[11].add_parent("127.0.0.8",-20,0)
	node_list[11].add_parent("127.0.0.9",-20,0)
	node_list[12].add_parent("127.0.0.10",-40,0)
	node_list[12].add_parent("127.0.0.11",-20,0)
	node_list[12].add_parent("127.0.0.12",-30,0)

	for i in range(len(node_list)):
		node_list[i].set_rank(i)
		#print((node_list[i].get_ip_address(),node_list[i].get_rank()))

	node_list[0].set_packet_rate(2)
	node_list[1].set_packet_rate(2)
	node_list[2].set_packet_rate(3)
	node_list[3].set_packet_rate(2)
	node_list[4].set_packet_rate(6)
	node_list[5].set_packet_rate(12)
	node_list[6].set_packet_rate(2)
	node_list[7].set_packet_rate(7)
	node_list[8].set_packet_rate(3)
	node_list[9].set_packet_rate(3)
	node_list[10].set_packet_rate(3)
	node_list[11].set_packet_rate(2)
	node_list[12].set_packet_rate(3)

	return node_list
