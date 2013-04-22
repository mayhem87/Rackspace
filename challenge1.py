#!/usr/bin/env python

import pyrax
import os
import time
from sys import argv
#Location of creds
creds = os.path.expanduser('~/.rackspace_cloud_credentials')

#Authentication
pyrax.set_credential_file(creds)


cs = pyrax.cloudservers
newservers = {}
script, name, amount = argv

#creating servers
print 'Here are your servers:'
for i in range(1,int(amount)+1):
	servername =  name+str(i)
	linux = cs.images.list()[28]
	ram = cs.flavors.list()[1]
	srvr = cs.servers.create(servername, linux.id, ram.id)
	newservers[servername] = srvr.id, srvr.adminPass

#displaying server info
for i,y in newservers.iteritems():
	info = cs.servers.get(y[0])
	while len(info.networks) == 0:
		time.sleep(30)
		info = cs.servers.get(y[0])
	print 'Name: ', i
	print 'IP: ', info.networks['public']
	print 'Admin Password: ', y[1]
	print '-'*10


