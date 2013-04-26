#!/usr/bin/env python

import os
import pyrax
import sys
import re

#Challenge 2: Write a script that clones a server 
#(takes an image and deploys the image as a new server).
#TO RUN
#./challenge2.py "id of server to image" "name of new server"

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)


cs = pyrax.cloudservers

self, sid, newname = sys.argv

try:
	server = cs.servers.get(sid)
except pyrax.exceptions.ServerNotFound, e:
	print 'Could not find server with id %s' % sid
	exit(0)

flavorid = server.flavor['id']
image_name = server.name + 'Image'


#Creating image

img_id = server.create_image(image_name)
print "Image '%s' is being created. Its ID is: %s" % (image_name, img_id)
image = cs.images.get(img_id)
pyrax.utils.wait_until(image,'status',['ACTIVE','ERROR','UNKNOWN'], interval=20, attempts=0)
image.get()
print 'Image is done'

#Creating server from image
ns = cs.servers.create(newname,img_id,flavorid)

#Giving info on new server
pyrax.utils.wait_until(ns, 'status',['ACTIVE','ERROR','UNKNOWN'], interval=10, attempts=0)
ns.get()
ip = re.search(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', str(servers.networks['public']))
print 'Here is your new server'
print 'Name: ', newname
print 'Admin Password: ', ns.adminPass
print 'IP: ', ip.group()

