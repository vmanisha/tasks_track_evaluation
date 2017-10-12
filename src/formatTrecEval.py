import os
import sys

def FormatTrecEvalResults(folder, outFolder):
    if not os.path.exists(outFolder):
        os.mkdir(outFolder)

    for ifile in os.listdir(folder):
        ofile = open(outFolder+'/'+ifile,'w')
        metric_dict = {}
        for line in open(folder+'/'+ifile,'r'):
            split = line.split('\t')
            # Format of trec_eval results.
            # Metric, Query, Value
            split[0] = split[0].strip()
            if split[1] not in metric_dict:
                metric_dict[split[1]] = {}
            metric_dict[split[1]][split[0]] = split[-1].strip()

        outStr = ''
        i = 0
        for queryId, metrics in metric_dict.items():
            if i == 0:
                ofile.write('topic,runid,'+','.join(sorted(metrics.keys()))+'\n')
                i+=1

            sorted_list = sorted(metrics.items())
            outStr = queryId+','+ifile
            for entry in sorted_list:
                outStr+=','+entry[1]
            ofile.write(outStr+'\n')
        ofile.close()

def main(argv):
    FormatTrecEvalResults(argv[1], argv[2])


if __name__ == '__main__':
    main(sys.argv)
