num=$1

serverId=(3 4 5 6 7 8 10 11 12 13)
for ((slave_num=0;slave_num<$num;slave_num++))
do
        screen_name=$"narsil-${serverId[$slave_num]}"
        screen -X -S $screen_name kill
done
