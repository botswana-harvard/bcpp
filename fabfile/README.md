
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
    
### options

`bootstrap_path` path to the `bootstrap.conf`. Usually `~/deployment/bcpp/bcpp/fabfile/conf/` where project repo is `bcppp`

`bootstrap_branch` git branch for `bootstrap.conf`. (Default `master`)

`release` release tag to deploy from. (Default: `None`)

`use_branch` force deployment from a branch instead of a release tag. (Default `False`)

`skip_pip_download` skips building the pip cache. (Default: `False`)

Example:
 
    fab -H localhost deploy.deployment_host:\
    bootstrap_path=~/deployment/bcpp/bcpp/fabfile/conf/,\
    bootstrap_branch=develop,use_branch=True,\
    release=develop,skip_pip_download=True

## deploy clients

Test connections, OS version, MYSQL version and nginx for `lentsweletau`:

    fab -R lentsweletau deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/

After tests inspect `~/lentsweletau.txt`

Deploy a client from the deployment host:

    fab -H <hostname> deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/

Deploy clients by role from the deployment host:
 
    fab -P -R <role> deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/

See `roledefs.py` in `bcpp.fabfile` for configured roles. Currently is by `map_area`.


Example:

    fab -H 192.168.157.16 deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=develop,bootstrap_branch=develop,map_area=lentsweletau --user=django

    
    
## deploy

    fab -H localhost git.cut_releases:source_root=/Users/erikvw/source/,project_repo_name=bcpp,requirements_file=requirements_production.txt --user=erikvw

    fab -H localhost deploy.deployment_host:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=0.1.13

    
