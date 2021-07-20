if  [ "$#" -ne 5  ]
then
    echo "Usage: $0 [pos1] [pos2] [pos3] [pos4] port"
    echo "Ex: $0 20 40 50 60 /dev/ttyUSB0"
    exit 1
fi

./listen.sh $5 && sleep 1 && ./send.sh $1 $2 $3 $4 $5
