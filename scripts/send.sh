# Setup serial port
stty -F /dev/ttyUSB0 9600 min 0 -icrnl -ixon -opost -echoctl -echoke -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke

echo "Sending position [$(($1 % 255)) $((2 % 255)) $(($3 % 255)) $(($4 % 255))] on $5"

printf "Received (a:success / f:fail): "
#listen in back ground for reply

sleep 1

#read -n 1 input < /dev/ttyUSB0 &


#compute crc
crc=$(($1 +$2 + $3 +$4))

#send msg to arduino
printf "##\\$(printf '%03o' "$1")\\$(printf '%03o' "$2")\\$(printf '%03o' "$3")\\$(printf '%03o' "$4")\\$(printf '%03o' "$crc")" > $5

#wait for reply
sleep 1
echo ""
killall tail
# #printf "\n"
# sleep 1

