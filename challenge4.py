#!/usr/bin/env python

import pyrax
import os
from sys import argv

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
dns = pyrax.cloud_dns

script, domain_name, ip  = argv

#Search for domain
try:
	dom = dns.find(name=domain_name)
#Create domain if not found
except pyrax.exceptions.NotFound:
	print 'Domain not found'
	print 'Creating domain'
	email = raw_input('Email address \n>')
	dom = dns.create(name=domain_name, emailAddress=email)	

#Create A record
a_rec = {'type' : 'A',
	'name' : domain_name,
	'data' : ip}

arec = dom.add_records(a_rec)
print "Created 'A' record for %s at %s" % (domain_name, ip)
