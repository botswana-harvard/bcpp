#!/bin/bash
echo "Dismounting Edc crypto keys"
# check if keys loaded
KEY_PATH=/Volumes/crypto_keys

if [ -d "$KEY_PATH" ]; then
         # 
         diskutil unmount /Volumes/crypto_keys
         echo 'dismounted Edc crypto keys.'
         date
 fi
 