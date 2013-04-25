#!/usr/bin/env python

import os
import sys
import pyrax

#Challenge 5: Write a script that creates a Cloud Database instance. 
#This instance should contain at least one database, and the database should 
#have at least one user that can connect to it.

#Creds
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cdb = pyrax.cloud_databases

#Syntax to run script
#./challenge5 'name of instance'

self, name= sys.argv

instance = cdb.create(name, flavor='2GB Instance', volume=10)
print 'Name: ', instance.name
print 'ID: ', instance.id

pyrax.utils.wait_until(instance, 'status', ['ACTIVE','ERROR','UNKNOWN'], interval=30)

db = instance.create_database('db1')
user = instance.create_user(name='default', password='default', database_names=[db])

print 'Database created: %s' % db.name
print 'Username: default'
print 'Password: default'

