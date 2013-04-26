#!/usr/bin/env python

import os
import pyrax
import sys
import time

#Challenge 8: Write a script that will create a static webpage served out of 
#Cloud Files. The script must create a new container, cdn enable it, enable it 
#to serve an index file, create an index file object, upload the object to the 
#container, and create a CNAME record pointing to the CDN URL of the container.


creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles

self, container, 

cont = cf.create_container(container)
cont.make_public(ttl=1200)

content = 'this is a web page'

obj = cf.store_object(cont, 'index.html', content, content_type = 'text/html')

