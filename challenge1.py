#!/usr/bin/env python

#Challenge 1: Write a script that builds three 512 MB Cloud Servers that 
#following a similar naming convention. (ie., web1, web2, web3) and returns 
#the IP and login credentials for each server. Use any image you want.

#How to run
#'./challenge1.py "server_name"'

import pyrax
import os
import re
from sys import argv
#Location of creds
creds = os.path.expanduser('~/.rackspace_cloud_credentials')

#Authentication
pyrax.set_credential_file(creds)

cs = pyrax.cloudservers
newservers = []
script, name = argv

#creating servers
print 'Here are your servers:'
for i in range(3):
	servername =  name+str(i+1)
	srvr = cs.servers.create(servername, '8bf22129-8483-462b-a020-1754ec822770', 3)
	newservers.append(srvr)

#displaying server info
for servers in newservers:
	pyrax.utils.wait_until(servers, 'status', ['ACTIVE', 'ERROR', 'UNKNOWN'], interval = 10, attempts=0)
	servers.get()
	ip = re.search(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', str(servers.networks['public']))
	print 'Name: ', servers.name
	print 'IP: root@' + ip.group()
	print 'Admin Password: ', servers.adminPass
	print '-'*10




