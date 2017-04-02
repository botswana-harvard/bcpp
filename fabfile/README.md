
1. place release conf files in a folder

    -- my_folder
        |-- bcpp.conf
        |-- device_ids.conf
        |-- secrets.conf

samples of each of these exist in `bcpp_fabric`

2. create a secure tarball: 

    cd my_folder    

    tar czvpf bcpp.conf secrets.conf device_ids.conf | gpg --symmetric --cipher-algo aes256 -o
    conf.tar.gz.gpg
    
3. save the passphrase.

4. copy the updated tarball to bcpp/fabric and commit to the repo.
    
5. to use or update:

    gpg -d conf.tar.gz.gpg | tar xzvf -
    
make your updates and create a new tarball and commit.

