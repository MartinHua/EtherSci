logname=$1
num=$2
pyPath="~/cs380D/EtherSci/slave.py"

for ((slave_num=0;slave_num<$num;slave_num++))
do
        screen_name=$"narsil-$[$slave_num+3]"
        screen -X -S $screen_name kill
done

for ((slave_num=0;slave_num<$num;slave_num++))
do
	screen_name=$"narsil-$[$slave_num+3]"
	screen -dmS $screen_name
	sshcmd="ssh $logname@narsil-$[$slave_num+3].cs.utexas.edu"
	pycmd=$"python3 $pyPath $slave_num 6000 $num 1"
	screen -x -S $screen_name -p 0 -X stuff "$sshcmd\n"
	screen -x -S $screen_name -p 0 -X stuff "$pycmd\n"
done

