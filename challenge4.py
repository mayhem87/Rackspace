#!/usr/bin/env python

import pyrax
import os
from sys import argv

#Challenge 4: Write a script that uses Cloud DNS to create a new A record 
#when passed a FQDN and IP address as arguments.

#HOW TO USE
#./challenge4.py "fqdn"

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
dns = pyrax.cloud_dns

script, fqdn, ip  = argv

#Search for domain
domain = fqdn.split('.')[-2] + '.' + fqdn.split('.')[-1]
try:
	dom = dns.find(name=domain)
#Create domain if not found
except pyrax.exceptions.NotFound:
	print 'Domain not found'
	print 'Creating domain'
	email = raw_input('Email address \n>')
	dom = dns.create(name=domain, emailAddress=email)	

#Create A record
a_rec = {'type' : 'A',
	'name' : fqdn,
	'data' : ip}

arec = dom.add_records(a_rec)
print "Created 'A' record for %s at %s" % (fqdn, ip)
