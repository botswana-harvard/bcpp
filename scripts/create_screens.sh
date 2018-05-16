#!/bin/bash

communities=(
"ranaka"
"digawana"
"molapowabojang"
"otse"
"letlhakeng"
"lentsweletau"
"bokaa"
"oodi"
"mmathethe"
"mankgodi"
"sefophe"
"lerala"
"ramokgonami"
"maunatlala"
"mmadinare"
"shoshong"
"metsimotlhabe"
"tati"
"sebina"
"nkange"
"mandunyane"
"mathangwane"
"rakops"
"gweta"
"shakawe"
"gumare"
"tsetsebjwe"
"sefhare"
"nata"
"masunga"
)
dex=0
length=${#communities[@]}
killall SCREEN
echo "creating screens for $length communities"
for i in ${communities[*]}
do
    echo "starting on $i"
    echo "index of $dex"
    screen -dm $i
#    cd ~/source/bcpp/ && source ~/.venvs/bcpp/bin/activate bcpp && python manage.py runserver 0.0.0.0:800
    echo "done creating screen for $i"
    ((dex++))
done
echo "done creating screens"

