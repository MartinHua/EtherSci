num=$1

for ((slave_num=0;slave_num<$num;slave_num++))
do
        screen_name=$"narsil-$[$slave_num+3]"
        screen -X -S $screen_name kill
done
