#!/usr/bin/env python

import os
import pyrax
import sys
import time
import re


creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
cf = pyrax.cloudfiles
dns = pyrax.cloud_dns
pu = pyrax.utils
rsa = open(os.path.expanduser('~/.ssh/id_rsa.pub'))
rsakey = rsa.read()
rsa.close()
files = {'/root/.ssh/authorized_keys': rsakey}
html = "<html><body>If you see this message please panic!</body></html>"

self, fqdn = sys.argv

servers = {}
for d in range(2):
	srv = 'srv' + str(d+1)
	servers[srv] = cs.servers.create(srv, '8bf22129-8483-462b-a020-1754ec822770', 3, files=files)

completed = []
while len(completed) < 2:
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

lb = clb.create(fqdn, port=80, protocol='HTTP', nodes=nlist, virtual_ips=[vip])

pu.wait_until(lb,'status', ['ACTIVE','ERROR'], interval = 5)

lb.add_health_monitor(type="CONNECT", delay=10, timeout=10, attemptsBeforeDeactivation=3)

time.sleep(10)

lb.set_error_page(html)

match = re.search(r'address=([\w.]+)', str(lb.virtual_ips))

print 'Load Balancer created'
print 'Load Balancer VIP: %s' % match.group(1)

domain = fqdn.split('.')[-2] + '.' + fqdn.split('.')[-1]

recs = [{
        "type": "A",
        "name": fqdn,
        "data": match.group(1),
        "ttl": 6000,
        }]

for domains in dns.list():
	if re.search(domain, str(domains)):
		domain = domains

domain.add_records(recs)

cont = cf.create_container("Backup")
obj = cf.store_object(cont, "LB_Error_Page.html", html, content_type='text/html')


print 'Done'



