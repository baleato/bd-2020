# /bin/bash

if [ ! -d ml-100k  ]; then
  wget http://files.grouplens.org/datasets/movielens/ml-100k.zip
  unzip ml-100k.zip
fi

if [ ! -d ml-1m  ]; then
  wget http://files.grouplens.org/datasets/movielens/ml-1m.zip
  unzip ml-1m.zip
fi

if [ ! -d ml-10M100K  ]; then
  wget http://files.grouplens.org/datasets/movielens/ml-10m.zip
  unzip ml-10m.zip
fi

run_script () {
  INTERVAL=1
  if [[ $2 == 'ml-1m' ]]; then
    INTERVAL=10
  fi
  if [[ $2 == 'ml-10m' ]]; then
    INTERVAL=100
  fi
  MODEL_NAME=$1-$2
  OUT=`mprof run --interval ${INTERVAL} --output ${MODEL_NAME}.dat run.py --dataset ${dataset} --output ${MODEL_NAME}.model ${algo}|grep -v -E 'mprof|running'`
  RAM=`cat ${MODEL_NAME}.dat | awk '{ print $2 }' | sort -n | tail -n 1`
  MODEL_SIZE=`ls -l ${MODEL_NAME}.model | awk '{ print $5 }'`
  echo ${algo},${dataset},`echo ${OUT} | awk '{ print $1","$2","$3","$4}'`,${RAM},${MODEL_SIZE}
  echo ${algo},${dataset},`echo ${OUT} | awk '{ print $1","$2","$3","$4}'`,${RAM},${MODEL_SIZE} >> out.csv
}

N=20

mprof clean
echo Algo,Dataset,Training time,Test time,RMSE,MAE,RAM,Model Size
echo Algo,Dataset,Training time,Test time,RMSE,MAE,RAM,Model Size >> out.csv
for dataset in ml-100k ml-1m ml-10m; do
  for algo in KNNWithMeans SVD NMF SlopeOne CoClustering; do
    (
      run_script "$algo" "$dataset"
      sleep $(( (RANDOM % 3) + 1))
    ) &

    # allow only to execute $N jobs in parallel
    if [[ $(jobs -r -p | wc -l) -gt $N ]]; then
        # wait only for first job
        wait -n
    fi
  done;
done

wait
echo "Done"
