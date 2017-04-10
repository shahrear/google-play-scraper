#if input 1 runs 1 to 100000
#if input 2 runs 100001 to 200000 ...


loopstart=$(($1-1))
loopstart=$((($loopstart*100000)+1))
loopmax=$(($1*100000))
for i in `seq $loopstart 10000 $loopmax`
      do
            bash run_parallel.sh $i
            echo -e "run parallel " $i
            echo -e "sleeping for 10 seconds done with 10000"
            sleep 10
      done
