loop1max=$(($1+9000))
#echo $loop1max
for parid in  `seq $1 1000 $loop1max`
  do
#        echo $parid
        loop2max=$(($parid + 900))
#        echo $loop2max
        for id in `seq $parid 100 $loop2max`
            do
                  node fetch_appinfo_mysql.js $id $(($id+99)) $id
                  echo -e $id $(($id+99)) $id
                  echo -e "sleeping for 1 seconds done with 100"
                  sleep 1
            done
      echo -e "sleeping for 5 seconds done with 1000"
      sleep 5
 done
