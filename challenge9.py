#!/usr/bin/env python

import os
import pyrax
import sys
import re

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

imglist =[]

for imgs in cs.images.list():
	if img_id.lower() in imgs.name.lower() or img_id in imgs.id:
			 imglist.append(imgs)

if len(imglist) > 1:
	print 'Please rerun script with one of the following as the image id'
	for x in imglist:
		print x.name, x.id
	exit(0)



srv = cs.servers.create(fqdn, imglist[0].id, flavor)

pyrax.utils.wait_until(srv, 'status', ['ACTIVE', 'ERROR'], interval=20)

srv.get()

domain = fqdn.split('.')[-2] + '.' + fqdn.split('.')[-1]

pip = ''

for ip in srv.networks['public']:
	if '.' in ip: pip = ip

recs = [{
        "type": "A",
        "name": fqdn,
        "data": pip,
        "ttl": 6000,
        }]

for domains in dns.list():
	if re.search(domain, str(domains)):
		domain = domains

domain.add_records(recs)

print 'Process finished'
print 'Server name %s' % srv.name
print 'Server ip %s' % pip
print 'Server password %s' % srv.adminPass




