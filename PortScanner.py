#!/usr/bin/python
import socket
import threading
import sys
from termcolor import colored
import getopt
from queue import Queue
import os
import time
opens=[]
def banner():
	os.system("clear")
	
	print '''
				
 ____            _   ____                                  
|  _ \ ___  _ __| |_/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
| |_) / _ \| '__| __\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
|  __/ (_) | |  | |_ ___) | (_| (_| | | | | | | |  __/ |   
|_|   \___/|_|   \__|____/ \___\__,_|_| |_|_| |_|\___|_|   

    '''
	l="\t\t\t\t\tBy Mbemekou Fred\n"
	u=""
	for b in l:
		u=u+b
		sys.stdout.write('\t\t\t\r'+u)
		sys.stdout.flush()
		time.sleep(0.01)

	print "\n\n"	
	time.sleep(0.1)
def usage():
	print (colored("./PortScanner.py -t <target_hosts> -p <target_ports>","green"))
	print ''' examples:
	./PortScanner.py -t 192.168.1.1 -p 20-2000
	./PortScanner.py -t 192.168.1.1-10 -p 80,443
	./PortScanner.py -t 192.168.1.1,192.168.1.110 -p 80


	'''
	sys.exit()
def scanner(host,port):
	global opens

	try:
		#print"socket creation"
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.settimeout(1)
		c=s.connect_ex((host,port))
		#print"c="
		#print c
		if(c==0):
			opens.append(port)
		else:
			sys.stdout.write("\r[*]scanning host: "+host+" on tcp port: "+str(port)+"                                          ")
			sys.stdout.flush()
		s.close()
	except Exception, e:
		print e
def testhost(host):
	global hosts_up
	if(not os.system("ping -c1 -w1  {} >/dev/null".format(host))):
		hosts_up.append(host)
def host_worker():
	while True:
		h=Q.get()
		if(h==None):
			Q.task_done()
			break
		testhost(h)
		Q.task_done()
def worker(host):
	
	while True:
		#print"waiting for worker"
		port=q.get()
		#print "worker {} got".format(port)
		if(port==None):
			q.task_done()
			break
		scanner(host,port)
		q.task_done()
def thread_handler(target_hosts,target_ports):
	global opens
	global threads
	for target_host in target_hosts:
		if target_host  not in  hosts_up:
			print (colored("[-] host  {}  down \n".format(target_host),"red"))
		else:

			opens=[]
			threads=[]
			
			for i in range(100):
				t=threading.Thread(target=worker,args=(target_host,))
				t.daemon=True
				t.start()
				#print"thead{} started".format(i)
				threads.append(t)
			for p in target_ports:
				q.put(p)
			q.join()
			#b=0
			for i in range(len(threads)):
				q.put(None)
				#b=b+1
				#print "put None on queue{}".format(b)
			#a=0
			for t in threads:
				t.join()
				#a=a+1
				#print("thread {} released".format(a))
			sys.stdout.write("                                                                 \n")
			if(not len(opens)):
				print("\n")
				print (colored("\n[-] host up but not opened ports found\n","blue"))
				print("\n")
			else:
				for port in opens:
					print (colored("\n[+] tcp/open {}".format(port),"green"))
				print "\n"

	


def start(argv):
	banner()
	if(len(argv)<4):
		usage()
		sys.exit()
	try:
		opts,args=getopt.getopt(argv[1:],"t:p:")
		
	except Exception,e:
		print e
		sys.exit()
	for o,a in opts:
		if o =="-t":
			try:
				targets=a
			except Exception,e:
				print e 
				sys.exit(0)

		elif o=="-p":
			try:
				ports=a
			except Exception,e:
					print e
					sys.exit(0)
		else:
			print "invalid options"
			sys.exit(0)
	target_hosts=[]
	if("-" in targets):
		ip_start=int(targets.split(".")[3].split("-")[0])
		ip_end=int(targets.split(".")[3].split("-")[1])
		subnet=targets.split(".")[0]+"."+targets.split(".")[1]+"."+targets.split(".")[2]
		for i in range(ip_start,ip_end+1):
			target_hosts.append(subnet+"."+str(i))
	elif("," in targets):
		target_hosts=targets.split(",").strip(' ')
		
	else:
		target_hosts.append(targets)
	target_ports=[]
	if("-" in ports):
		port1=int(ports.split("-")[0])
		port2=int(ports.split("-")[1])
		for port in range(port1, port2+1):
			target_ports.append(port)

	elif("," in ports):
		portraw=ports.split(",")
		for i in portraw:
			target_ports.append(int(i))
	else:
		target_ports.append(int(ports))
	global threadss
	for i in range(25):
		t=threading.Thread(target=host_worker)
		t.daemon=True
		t.start()
		threadss.append(t)
	for host in target_hosts:
		Q.put(host)

	Q.join()
	for i in range(len(threadss)):
		Q.put(None)
	for t in threadss:
		t.join()
	
	thread_handler(target_hosts,target_ports)
Q=Queue()
q=Queue()
threads=[]
threadss=[]
hosts_up=[]
start(sys.argv)

