#!/usr/bin/env python

import os
import sys
import pyrax

#Creds
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cdb = pyrax.cloud_databases

#Syntax to run script
#./challenge5 'name of instance' 'flavor' 'storage size 1-50GB'

self, name, ram, gb = sys.argv

#Flavors by number
#0 = 512MB
#1 = 1GB
#2 = 2GB
#3 = 4GB
flav = cdb.list_flavors()[int(ram)]

instance = cdb.create(name, flavor=flav, volume=gb)
print 'Name: ', instance.name
print 'ID: ', instance.id
print 'Status: ', instance.status

pyrax.utils.wait_until(instance, 'status', 'ACTIVE',interval=30)

db = instance.create_database('db1')
user = instance.create_user(name='default', password='default', database_names=[db])

