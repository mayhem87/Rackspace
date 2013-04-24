#!/usr/bin/env python

import os
import pyrax
import sys
import time

#Challenge 3: Write a script that accepts a directory as an argument as well as 
#a container name. The script should upload the contents of the specified 
#directory to the container (or create it if it doesn't exist). The script 
#should handle errors appropriately. (Check for invalid paths, etc.) 


#HOW TO RUN
#./challenge3.py "directory path" "name of container"

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles

self, direct, cnm = sys.argv
completed = None

try:
	key, size = cf.upload_folder(direct, container=cnm)
	print 'Uploading %s to %s. File size is %d' % (direct, cnm, size) 
except KeyboardInterrupt:
	print 'Aborting upload'
	cf.cancel_folder_upload(key)
	exit(0)
except pyrax.exceptions.FolderNotFound:
	print 'Invalid path' 
	exit(0)

while completed < size:
	try:
		completed = pyrax.cloudfiles.get_uploaded(key)
		time.sleep(30)
		print '{0:.0%}'.format(float(completed)/float(size))
	except KeyboardInterrupt:
		print 'Aborting upload'
		cf.cancel_folder_upload(key)
		exit(0)
	except pyrax.exceptions.FolderNotFound:
		print 'Invalid path' 
		exit(0)	