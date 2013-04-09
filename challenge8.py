#!/usr/bin/env python

import os
import pyrax
import sys
import time

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles

self, container, 

cont = cf.create_container(container)
cont.make_public(ttl=1200)

content = 'this is a web page'

obj = cf.store_object(cont, 'index.html', content, content_type = 'text/html')

