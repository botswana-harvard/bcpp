#!/bin/bash
echo "Loading the Edc crypto keys"
cd /Users/django/prep_notebook && hdiutil attach -stdinpass crypto_keys.dmg

# check if keys loaded
KEY_PATH=/Volumes/crypto_keys

if [ -d "$KEY_PATH" ]; then
         echo 'Edc crypto keys loaded successfully.'
         date
         sh /Users/django/source/bash_scripts/gunicorn_startup.sh
 else
   echo "Failed to load Edc crypto keys. "
 fi
 