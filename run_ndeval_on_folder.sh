if [ $# -eq 0 ]
  then
    echo 'Please pass [run-folder] [output-folder] [qrel]'
    exit 1
fi

if [ -z "$1" ]
  then
    echo "No document run folder supplied. Please pass [run-folder] [output-folder] [qrel]"
    exit 1
fi
mkdir $2;
for fname in `ls $1`
do
	file=$1$fname
        #./eval/trec_eval.9.0/trec_eval -m all_trec -q $3 $file > $2$fname
	./eval/diversity_eval/ndeval $3 $file > $2$fname
done
