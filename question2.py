#!/usr/bin/env python

import os
import pyrax
import time


creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)


cs = pyrax.cloudservers
servers = cs.servers.list()
srv_dict = {}

#Selection of server to image
def build():
	srv_image = raw_input('Please type name of target server.\n> ')
	srv_dict.clear()
	for i, x in enumerate(servers):
		if srv_image in str(x).lower():
        		print '%s: %s' % (i+1, x.name)
                	srv_dict[str(i+1)] = x.id

build()

#Checks to see if choice is valid
sel = 'none'
while sel not in srv_dict:
    	if sel == str(0):
		build()
        elif sel is not 'none':
		print 'Invalid please choose again'
	print 'If server not found enter 0'	
    	sel = raw_input("Enter the number for your choice: ")

#Server id and flavor to be used later
sid = srv_dict[sel]
flavorid = cs.servers.get(sid).flavor['id']

#Creating image
nm = raw_input('Enter a name for the image: ')
img_id = cs.servers.create_image(sid, nm)
print "Image '%s' is being created. Its ID is: %s" % (nm, img_id)
while cs.images.get(img_id).status != 'ACTIVE':
	time.sleep(30)
print 'Image is done'

#Creating server from image
newname = raw_input('Name of clone server?\n> ')
ns = cs.servers.create(newname,img_id,flavorid)

#Giving info on new server
ip = cs.servers.get(ns.id)
while len(ip.networks) == 0:
	time.sleep(30)
	ip = cs.servers.get(ns.id)
print 'Here is your new server'
print 'Name: ', newname
print 'Admin Password: ', ns.adminPass
print 'IP: ', ip.networks['public']


