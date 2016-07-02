import lib.DataStructures
import lib.FetchNetwork
import lib.RRDListener
import rrdtool
import threading 
import time
import socket
lock=threading.Lock()
UDP_IP="aaaa::1"
UDP_PORT=5678
class FetchNetworkThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		try:
			lib.FetchNetwork.init()
			lib.DataStructures.event.set()
			while(True):
				lock.acquire()
				lib.FetchNetwork.init()
				lock.release()
				time.sleep(15)
		except KeyboardInterrupt:
			print("Program Terminated")
			sys.exit()



class RRDListenerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		try:
			lib.RRDListener.init(lock)				
			#while(True):
				#lib.RRDListener.init()				
		except KeyboardInterrupt:
			print("Program Terminated")
			sys.exit()

"""
class UDPServerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		try:
			sock=socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
			sock.bind((UDP_IP,UDP_PORT))
			print "UDP Server Started"
			while True:
				data, addr = sock.recvfrom(30)
				lib.DataStructures.udp_packets_received_from_network=lib.DataStructures.udp_packets_received_from_network+1
		except KeyboardInterrupt:
			print("Program Terminated")
			sys.exit()
"""



fetch_network_thread=FetchNetworkThread()
rrd_listener_thread=RRDListenerThread()
#udp_server_thread=UDPServerThread()
fetch_network_thread.daemon=True
rrd_listener_thread.daemon=True
#udp_server_thread.daemon=True

fetch_network_thread.start()
#udp_server_thread.start()
while not lib.DataStructures.event.is_set():
	continue
time.sleep(60)
rrd_listener_thread.start()


try:
	while True:
		lock.acquire()
		print("RRD Graph Plotting")
		ret = rrdtool.graph( "lib/rrd_graphs/packet_rate.png", "--start", "-3600", "--vertical-label=Num",
		'--watermark=Path Computation ',
		"--slope-mode",
		"--no-gridfit",
		"--title=Packet Rates",
		"-w 1000",
		"-h 600",
		"--alt-autoscale",
		"DEF:m1_num=lib/rrd/packet_rate.rrd:NodeId-2:AVERAGE",
		"DEF:m2_num=lib/rrd/packet_rate.rrd:NodeId-3:AVERAGE",
		"DEF:m3_num=lib/rrd/packet_rate.rrd:NodeId-4:AVERAGE",
		"DEF:m4_num=lib/rrd/packet_rate.rrd:NodeId-5:AVERAGE",
		"DEF:m5_num=lib/rrd/packet_rate.rrd:NodeId-6:AVERAGE",
		#"DEF:m6_num=lib/rrd/packet_rate.rrd:NodeId-7:AVERAGE",
		#"DEF:m7_num=lib/rrd/packet_rate.rrd:NodeId-8:AVERAGE",
		#"DEF:m8_num=lib/rrd/packet_rate.rrd:NodeId-9:AVERAGE",
		"LINE4:m1_num#a6cee3:aaaa\:\:200\:0\:0\:2",
		"LINE4:m2_num#1f78b4:aaaa\:\:200\:0\:0\:3",
		"LINE4:m3_num#b2df8a:aaaa\:\:200\:0\:0\:4",
		#"LINE4:m4_num#33a02c:aaaa\:\:200\:0\:0\:5")
		"LINE4:m4_num#33a02c:aaaa\:\:200\:0\:0\:5",
		"LINE4:m5_num#fb9a99:aaaa\:\:200\:0\:0\:6")
		#"LINE4:m6_num#e31a1c:aaaa\:\:200\:0\:0\:7")
		#"LINE4:m7_num#fdbf6f:aaaa\:\:200\:0\:0\:8")
		#"LINE4:m8_num#ff7f00:aaaa\:\:200\:0\:0\:9")

		ret = rrdtool.graph( "lib/rrd_graphs/packet_delivery_rate.png", "--start", "-3600", "--vertical-label=Num",
		'--watermark=Path Computation ',
		"--slope-mode",
		"--title=Packet Rates",
		"-w 1000",
		"-h 400",
		"--upper-limit=100",
		"--lower-limit=94",
		"--rigid",
		#"--color=CANVAS#000000",
		#"--color=GRID#FFFFFF",
		"--alt-autoscale-min",
		"--no-gridfit",
		"DEF:avg=lib/rrd/packet_delivery_rate.rrd:pdr:AVERAGE",
		"AREA:avg#004D4D77:Average Network PDR",
		"LINE3:avg#004D4D")
		lock.release()
		time.sleep(15)
except KeyboardInterrupt:
	print("Program Terminated")
	
