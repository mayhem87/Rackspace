#!/usr/bin/env python

import os
import pyrax
import sys
import time

#Challenge 13: Write an application that nukes everything in your Cloud Account. It should:
#Delete all Cloud Servers
#Delete all Custom Images
#Delete all Cloud Files Containers and Objects
#Delete all Databases
#Delete all Networks
#Delete all CBS Volumes

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
dns = pyrax.cloud_dns
cbs = pyrax.cloud_blockstorage
cf = pyrax.cloudfiles
cdb = pyrax.cloud_databases
cnw = pyrax.cloud_networks


print 'Deleting Servers'
for servers in cs.servers.list():
	servers.delete()

print 'Deleting Storage'
for storage in cbs.list():
	storage.delete()

print 'Deleting Cloudfiles'
for container in cf.get_all_containers():
	container.delete_all_objects()
	container.delete()

print 'Deleting Databases'
for db in cdb.list():
	db.delete()

print 'Deleting Networks'
networklist = [ 'public', 'private' ]
for network in cnw.list():
	if network.name not in networklist:
		network.delete()

print 'Deleting Imagges'
for images in cs.images.list()
	images.delete()