logname=$1
num=$2
port=$3

pyPath="/u/xh3426/cs380D/EtherSci/slave.py"

serverId=(3 4 5 6 7 8 10 11 12 13)
for ((slave_num=0;slave_num<$num;slave_num++))
do
        screen_name=$"narsil-${serverId[$slave_num]}"
        screen -X -S $screen_name kill
done

for ((slave_num=0;slave_num<$num;slave_num++))
do
	screen_name=$"narsil-$[$slave_num+3]"
	screen -dmS $screen_name
	sshcmd="ssh $logname@narsil-${serverId[$slave_num]}.cs.utexas.edu"
	pycmd=$"python3 $pyPath $slave_num $port $num 1"
	screen -x -S $screen_name -p 0 -X stuff "$sshcmd\n"
	screen -x -S $screen_name -p 0 -X stuff "$pycmd\n"
done

