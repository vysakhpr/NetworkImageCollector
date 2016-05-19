import socket
import lib.DataStructures
import sys

def init(graph_nodes):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((lib.DataStructures.nme_ip,lib.DataStructures.nme_port))
	while True:
		s.listen(1)
		conn,addr=s.accept()
		print len(graph_nodes)
		conn.send(str(len(graph_nodes)))
		conn.close()
		for node in graph_nodes:
			conn,addr=s.accept()
			buff=""
			buff=buff+str(node.get_ip_address())+";"+str(node.get_rank())+";"+str(node.get_packet_rate())+";"
			for parent in node.get_parent_list():
				buff=buff+parent+";"
			print buff
			conn.send(buff)
			conn.close()


		