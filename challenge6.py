#!/usr/bin/env python

import pyrax
import sys
import os

#Challenge 6: Write a script that creates a CDN-enabled container in Cloud Files.

#HOW TO RUN
#./challenge6.py "container name"

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles


self, cnm = sys.argv

if cnm in cf.list_containers():
	print 'Container already exists'
else:
	cont = cf.create_container(cnm)
	cont.make_public(ttl=1200)
	print "cdn_enabled", cont.cdn_enabled
	print "cdn_ttl", cont.cdn_ttl
	print "cdn_log_retention", cont.cdn_log_retention
	print "cdn_uri", cont.cdn_uri
	print "cdn_ssl_uri", cont.cdn_ssl_uri
	print "cdn_streaming_uri", cont.cdn_streaming_uri
