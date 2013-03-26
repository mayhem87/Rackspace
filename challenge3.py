#!/usr/bin/env python

import os
import pyrax
import sys


creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles

self, direct, cnm = sys.argv

try:
	key, size = cf.upload_folder(direct, container=cnm)
	print 'Uploading %s to %s. File size is %d' % (direct, cnm, size)
		 
except KeyboardInterrupt:
	cf.cancel_folder_upload(key)

except pyrax.exceptions.FolderNotFound:
	print 'Invalid path' 
