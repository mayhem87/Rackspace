#!/usr/bin/env python

import sys
import os
import pyrax
import time

#Challenge 7: Write a script that will create 2 Cloud Servers and add them as 
#nodes to a new Cloud Load Balancer.

#HOW TO USE
#./challenge7.py 'server name' 'name of loadbalancer'

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

self, snm, lbname = sys.argv

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
flav = 2
img_id = '8bf22129-8483-462b-a020-1754ec822770'

completed = []

for i in range(2):
	name = '%s%s' % (snm, i+1)
	server = cs.servers.create(name,img_id,flav)
	completed.append(server)

for server in completed:
	pyrax.utils.wait_until(server, 'status', ['ACTIVE','ERROR', 'UNKNOWN'])
	server.get()
	print 'Server Completed'
	print 'ID: %s' % server.id
	print 'Networks: %s' % server.networks
	print 'Password: %s' % server.adminPass
		
nlist = []

for server in completed:
	nlist.append(clb.Node(address=server.networks['private'][0], port=80, condition='ENABLED'))		

vip = clb.VirtualIP(type='PUBLIC')

print 'Creating Load Balancer'

lb = clb.create(lbname, port=80, protocol='HTTP', nodes=nlist, virtual_ips=[vip])

print 'Load Balancer Created'
print 'Public IPs: ', lb.virtual_ips
