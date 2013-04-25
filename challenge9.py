#!/usr/bin/env python

import os
import pyrax
import sys
import re

#Challenge 9: Write an application that when passed the arguments FQDN, 
#image, and flavor it creates a server of the specified image and flavor with 
#the same name as the fqdn, and creates a DNS entry for the fqdn pointing to the 
#server's public IP.

#HOW TO RUN
#./challenge9.py 'fqdn' 'image id' 'flavor'

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
dns = pyrax.cloud_dns

self, fqdn, img_id, flavor = sys.argv

#QUICK reference for flavors:
# 512MB Standard Instance 2
# 1GB Standard Instance 3
# 2GB Standard Instance 4
# 4GB Standard Instance 5
# 8GB Standard Instance 6
# 15GB Standard Instance 7
# 30GB Standard Instance 8

srv = cs.servers.create(fqdn, img_id, flavor)

pyrax.utils.wait_until(srv, 'status', ['ACTIVE', 'ERROR', 'UNKNOWN'], interval=20)

srv.get()

domain = fqdn.split('.')[-2] + '.' + fqdn.split('.')[-1]

re_ip = re.search(r'[\d.]+', str(srv.networks['public']))
ip = re_ip.group()

recs = [{
        "type": "A",
        "name": fqdn,
        "data": ip,
        "ttl": 6000,
        }]

for domains in dns.list():
	if re.search(domain, str(domains)):
		domain = domains

domain.add_records(recs)

print 'Process finished'
print 'Server name %s' % srv.name
print 'Server ip %s' % ip
print 'Server password %s' % srv.adminPass




