
encrypt the secrets.conf

    gpg -o secrets.conf.gpg --cipher-algo AES256 --symmetric secrets.conf
    
save the passphrase.

decrypt

    gpg -d secrets.conf.gpg > secrets.conf
    
encrypt the hosts.conf

    gpg -o hosts.conf.gpg --cipher-algo AES256 --symmetric hosts.conf
    
save the passphrase.

decrypt

    gpg -d hosts.conf.gpg > hosts.conf
    
    
## set up the deployment host

Using the bootstrap.conf in the bcpp repo:
    
    fab -H localhost deploy.deployment_host:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/
    

## deploy clients

Test connections, OS version, MYSQL version and nginx for `lentsweletau`:

    fab -R lentsweletau deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/

After tests inspect `~/lentsweletau.txt`

Deploy a client from the deployment host:

    fab -H <hostname> deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/

Deploy clients by role from the deployment host:
 
    fab -P -R <role> deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/

See `roledefs.py` in `bcpp.fabfile` for configured roles. Currently is by `map_area`.
