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
dns = pyrax.cloud_dns
cbs = pyrax.cloud_blockstorage

#Challenge 11: Write an application that will:
#Create an SSL terminated load balancer (Create self-signed certificate.)
#Create a DNS record that should be pointed to the load balancer.
#Create Three servers as nodes behind the LB.
#     Each server should have a CBS volume attached to it. (Size and type are irrelevant.)
#     All three servers should have a private Cloud Network shared between them.
#     Login information to all three servers returned in a readable format as the result of the script, 
#	  including connection information.

#HOW TO RUN:
#./challenge11.py 'fqdn'

self, fqdn = sys.argv

completed = []

for d in range(3):
	name = 'srv' + str(d+1)
	server = cs.servers.create(name, '8bf22129-8483-462b-a020-1754ec822770', 3)
	completed.append(server)

nlist = []
for server in completed:
	pyrax.utils.wait_until(server,'status',['ACTIVE','ERROR'],interval=25)
	server.get()
	vol = cbs.create(name=server.name, size=500, volume_type="SATA")
	vol.attach_to_instance(server.id, mountpoint="/dev/xvdb")
	nlist.append(clb.Node(address=server.networks['private'][0], port=80, condition='ENABLED'))		
	print 'Server completed'
	print 'Server name %s' % server.name
	print 'Server password %s' % server.adminPass
	print 'Server Public IP %s' % server.networks['public']

vip = clb.VirtualIP(type='PUBLIC')

lb = clb.create('LB2', port=80, protocol='HTTP', nodes=nlist, virtual_ips=[vip])


#SSL Cert and Key Handling 
#Key and cert for example only

key = """
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDMRUszCaKiWKbdDtKoKSQDIbDKdp6PRT6CSnV9H/KIbDRR1wZd
wydoVOVJ0HTc2lK+IK37LweKpYIiz1hcDAmkFNc7MGnhO0Ij/7TA3384e8IFS2Im
LYFXt4kVA2cwPOVbDJBMcBL62gDUgGOKWIYZo8krSKPZffBIDNoKSMwfqQIDAQAB
AoGAFjbG6cL3e742Tz3obL8kmm6UgkAKGDyIgrTEOBo8TtetjOTcXV/2riLlWHSh
8M6RRvnY0cMYh9xd3Zk82623cn3G24wUwouJPzY+nKBOgIW9XwqY2ssV+RPCaGvq
xphyENhcXWCzIc4C6DFU3J4ufW46bAA10WyXXBew+INMAZ0CQQDuAQoaU+gPc8Jc
GPm0tqQXSwLm5yHCdBY2YG3LOd93uTu6qh9Iet14Q8GgqAPAxQIIKsJ/WRueAZMG
iU+8yphDAkEA27dKBEtmP61hVYZ7c4Qx0eqI/CMt8YsvRFRKCC5f655fYqqF6PfA
PJugB6xek56fic7SJvD0mgpXPIQWKyXPowJADVIZkqenkVXVRvpO34JpZLRaETpW
dV+x7pEvE/TFQRoo8aWb4p6dzqFcMPW2YA+msXZTNHV0Sj+kTvVYdSSRqQJBAICZ
tGn1E+Dbg2gCsck4K8zZANrLYH3LYJwW1coaEqyfYucmNgDY2hzfXfh/zE+M/YY0
ls6SJCjxOoRCL5OLqw8CQQDs0y8hrjElAwhMQSNO3fffKJier1Qb1YNsme0klkrw
G5PChv+DOHg9TgLl0JEnyyYJ0rZsSH6ypDu+SjQtweTl
-----END RSA PRIVATE KEY-----
"""

cert = """
-----BEGIN CERTIFICATE-----
MIIB/zCCAWgCCQDsF5AeCVO5WzANBgkqhkiG9w0BAQUFADBEMQswCQYDVQQGEwJV
UzEOMAwGA1UECAwFVGV4YXMxFDASBgNVBAcMC1NhbiBBbnRvbmlvMQ8wDQYDVQQK
DAZNQVlIRU0wHhcNMTMwNDE3MTc1NDQzWhcNMTQwNDE3MTc1NDQzWjBEMQswCQYD
VQQGEwJVUzEOMAwGA1UECAwFVGV4YXMxFDASBgNVBAcMC1NhbiBBbnRvbmlvMQ8w
DQYDVQQKDAZNQVlIRU0wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMxFSzMJ
oqJYpt0O0qgpJAMhsMp2no9FPoJKdX0f8ohsNFHXBl3DJ2hU5UnQdNzaUr4grfsv
B4qlgiLPWFwMCaQU1zswaeE7QiP/tMDffzh7wgVLYiYtgVe3iRUDZzA85VsMkExw
EvraANSAY4pYhhmjyStIo9l98EgM2gpIzB+pAgMBAAEwDQYJKoZIhvcNAQEFBQAD
gYEAA+Wh+DK9opC5NfN76PC0NByVfVknHEmUmYXutkqELPlu3oFerrnNJ9adRNfQ
H4Gi94kRB6EpdSp15AcOZFPTVNidvzx1bu7aEYGUUFyftFAgOdEBnxWOMH7s6jzd
laEk5u4XUc5rHwa2cC7N1g6ZRw6/k1TnItkWiJbLxLrkPYQ=
-----END CERTIFICATE-----
"""

#Example of loading from file
#with open('./filename.crt') as private
#	key = private.read()

pyrax.utils.wait_until(lb, 'status', ['ACTIVE','ERROR'], interval=10)

lb.add_ssl_termination( securePort=443, enabled=True, secureTrafficOnly=False, certificate=cert, privatekey=key )

match = re.search(r'address=([\w.]+)', str(lb.virtual_ips))

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


