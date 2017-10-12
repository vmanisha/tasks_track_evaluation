import os
import argparse as ap
import sys
import pandas as pd


def RunNdEval(qrelFile,runFolder, outFolder):
    docTopics= range(1,51)
    # used for 2015: [1, 2 ,3 ,4 ,5 ,6 ,7, 8, 9, 11, 12, 14 ,15 ,16, 17 ,18 ,19 ,20, 21, 22, 23, 24, 25, 26, 28, 29, 31, 32, 34, 35, 36, 37, 42, 43, 50]
    commandString = 'perl ./eval/diversity_eval/gdeval.pl '
    if not os.path.exists(outFolder):
        os.mkdir(outFolder)
    for ifile in os.listdir(runFolder):
        run  = open(runFolder+'/'+ifile,'r').read()
        step = 5
        k = 5
        runMetrics = {}
        runid = None
        # Format :
        # runid,topic,ndcg@K,err@K
        for k in [10,20,1000]:
            print k, ifile
            # Run the command
            print commandString+' -k '+str(k)+' '+qrelFile+' '+runFolder+'/'+ifile
            content = os.popen(commandString+' -k '+str(k)+' '+qrelFile+' '+runFolder+'/'+ifile).read()
            # Process and store the input
            i= 0
            header = {}
            #print content
            for line in content.split('\n'):
                split = line.strip().split(',')
                if len(split) == 4:
                    # Set the header
                    if i == 0:
                        for l in range(len(split)):
                            header[l] = split[l]
                        i+=1
                    else:
                        runid = split[0]
                        topic = split[1]
                        if 'amean' in topic or int(topic) in docTopics:
                            if topic not in runMetrics:
                                runMetrics[topic] = {}
                            runMetrics[topic][header[2]] = split[2]
                            runMetrics[topic][header[3]] = split[3]
        ofile = open(outFolder+'/'+ifile,'w')
        # write the header
        #dataFrame = pd.DataFrame(index= range(1,50), columns= runMetrics['amean'].keys())
 
        ofile.write('runid,topic,'+','.join(sorted(runMetrics['amean'].keys()))+'\n')
        for entry in sorted(runMetrics.items()):
            topic, metricValues = entry[0], entry[1]
            sortedMet = sorted(metricValues.items())
            #print topic, sortedMet
            values  = []
            for entry in sortedMet:
                values.append(entry[1])
            #print values 
            ofile.write(runid+','+topic+','+','.join(values) +'\n')
        ofile.close()


def main(argv):
    parser = ap.ArgumentParser(description='Generate diversity evaluation for several runs in a folder');
    parser.add_argument('-q','--qrelFile', help='Qrel file to use for evaluation. Should have format \
                                                query-id subtopic-id doc-id relevance', required=True);
    parser.add_argument('-r','--runFolder', help='Folder containing participant runs.', required=True);
    parser.add_argument('-o','--outFolder', help='Folder to output per query evaluation for each submitted run.', required=True);
    args = parser.parse_args()
    RunNdEval(args.qrelFile, args.runFolder, args.outFolder)

if __name__ == '__main__':
    main(sys.argv)
