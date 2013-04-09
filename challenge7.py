#!/usr/bin/env python

import sys
import os
import pyrax
import time

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

self, snm, number, lbname = sys.argv

#Run challenge7.py 'server name' '# of servers' 'name of loadbalancer'
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
flav = 2
img_id = '8bf22129-8483-462b-a020-1754ec822770'
number = int(number)


servers = {}
for i in range(0, number):
	name = '%s%s' % (snm, i+1)
	servers[name] = cs.servers.create(name,img_id,flav)

completed = []
while len(completed) < number:
	time.sleep(30)
	for server in servers.values():
		if server in completed:
			continue
		server.get()
		if server.status in ['ACTIVE', 'ERROR', 'UNKNOWN']:
			print 'Server Completed'
			print 'ID: %s' % server.id
			print 'Networks: %s' % server.networks
			print 'Password: %s' % server.adminPass
			completed.append(server)


nlist = []

for server in completed:
	nlist.append(clb.Node(address=server.networks['private'][0], port=80, condition='ENABLED'))		
vip = clb.VirtualIP(type='PUBLIC')

lb = clb.create(lbname, port=80, protocol='HTTP', nodes=nlist, virtual_ips=[vip])

