# tasks_track_evaluation

Evaluation scripts used for tasks track 2016 (http://www.cs.ucl.ac.uk/tasks-track-2016/)


PROCEDURE TO GENERATE METRICS
-----------------------------

Following types of evaluation needs to be conducted:

Adhoc evaluation:
-----------------
Please follow the following steps to generate adhoc metrics for submitted runs.
a. make_dir.sh
b. cut -d' ' -f1,2,3,5 qrel-docs.txt > qrels-utility-doc.txt
c. cut -d' ' -f1,2,3,4 qrel-docs.txt > qrels-relevance-doc.txt

For 2016, we had to remove documents with -3 label from evaluation. The following command was used:
 grep -P -v '\-3$' qrels-utility-doc.txt > qrels-utility-doc-without-minus-3.txt 
Dont forget to replace -2 label with 0. 

a. Run following command to generate the numbers:
 python src/runGdEval.py -q qrels/qrels-adhoc-rel-docs-without-minus-3.txt -r doc-runs/adhoc/ -o rel-adhoc-eval/
b. Find min/max/mean using the following command:
  python src/minMaxAverageRuns.py -f rel-adhoc-eval/ -o adhoc_retrieval.txt


Diversity evaluation:
-----------------
Get the diversity evaluation for KEYWORDS:
a. sh run_ndeval_on_folder.sh keyword-runs-trec-eval-format/ keyword-diversity-eval/ qrels/keyword-qrel-trec-eval-format.txt
b. python src/minMaxAverageRuns.py -f keyword-diversity-eval/ -o task_understanding.txt

All the outputs (per run evaluation, min, max and mean of each query computed using all runs) are in folder keyword-diversity-eval

Get the diversity evaluation for RELEVANCE:
a. sh run_ndeval_on_folder.sh doc-runs/diversity/ rel-diversity-eval/ qrels/qrels-rel-doc-without-minus-3.txt 
b.  src/minMaxAverageRuns.py -f rel-diversity-eval/ -o task_completion.txt

Get Diversity evaluation for Utility:
a. sh run_ndeval_on_folder.sh doc-runs/diversity/ utility-diverse-eval/ qrels/qrels-utility-doc-without-minus-3.txt
b. python src/minMaxAverageRuns.py -f utility-diverse-eval/ -o utility.txt

-----------------------------------
Relevance and Utility Distribution for 2016.
-----------------------------------

Relevance Labels:
24184 0
4673 1
394 2
762 -2

Utility Labels:
29444 0
3799 1
282 2

-----------
QREL FORMAT
-----------

The format of the qrels file for key phrases is
     topic-id subtask-id judgment key-phrase
where key-phrase may have embedded white space.

The format of the qrels file for documents is
     topic-id subtask-id docno rel-judgment utility-judgment

