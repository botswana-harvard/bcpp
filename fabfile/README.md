
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