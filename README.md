# PortScanner
simple  pythonic  quick port scanner

PortScanner is a simple tool written in python to help you scan network.

Author: Mbemekou Fred

Requirements: Python 2.7.x

Install apt-get -y install git

git clone https://github.com/mbemekou/PortScanner.git

cd ./PortScanner

chmod +x PortScanner.py

/PortScanner.py -t <target_hosts> -p <target_ports>

 examples:
 
        ./PortScanner.py -t 192.168.1.1 -p 20-2000
        
        ./PortScanner.py -t 192.168.1.1-10 -p 80,443
        
        ./PortScanner.py -t 192.168.1.1,192.168.1.110 -p 80
        

