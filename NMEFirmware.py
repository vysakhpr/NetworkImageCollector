import  lib.DataStructures
import lib.FetchNetwork
import lib.test.BuildNetworkDemo
import lib.PceListener

import threading
import time

graph_nodes=[]

class FetchNetworkThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global graph_nodes
		graph_nodes=lib.FetchNetwork.init(graph_nodes,"coapthon")
		lib.DataStructures.event.set()
		time.sleep(20)
		try:
			while(True):
				graph_nodes=lib.FetchNetwork.init(graph_nodes,"coapthon")
				time.sleep(20)
		except KeyboardInterrupt:
			print("Program Terminated")
			sys.exit()



class PceListenerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global graph_nodes
		try:
			while(True):
				lib.PceListener.init(graph_nodes)				
		except KeyboardInterrupt:
			print("Program Terminated")
			sys.exit()



lib.DataStructures.event.clear()



fetch_network_thread=FetchNetworkThread()
pce_listener_thread=PceListenerThread()
fetch_network_thread.daemon=True
pce_listener_thread.daemon=True

fetch_network_thread.start()
#graph_nodes=lib.FetchNetwork.init(graph_nodes,"coapthon")
#graph_nodes=lib.FetchNetwork.init(graph_nodes,"txthings")
#graph_nodes=lib.test.BuildNetworkDemo.initDemoTwo();
while not lib.DataStructures.event.is_set():
	continue

pce_listener_thread.start()



try:
	while True:
		continue
except KeyboardInterrupt:
	print("Program Terminated")
	