for i in `seq 31 35`
      do
            bash run_parallel_thousands.sh $i &
      done
wait

for i in `seq 36 40`
      do
            bash run_parallel_thousands.sh $i &
      done
wait

for i in `seq 41 45`
      do
            bash run_parallel_thousands.sh $i &
      done
wait


for i in `seq 46 50`
      do
            bash run_parallel_thousands.sh $i &
      done
wait


for i in `seq 51 53`
      do
            bash run_parallel_thousands.sh $i &
      done
wait


for i in `seq 1 30`
      do
            bash run_parallel_thousands.sh $i &
      done
wait
