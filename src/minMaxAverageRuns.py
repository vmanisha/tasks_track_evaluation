import os
import pandas as pd
import sys
import numpy as np
import argparse as ap

def FindMinMaxAvg(folderName, outFile):
    dataDict = {}
    for ifile in os.listdir(folderName):
        print 'Finished reading ',ifile
        data = pd.read_csv(folderName+'/'+ifile);
        dataDict[ifile] = data;
        print 'Columns in each evaluation file ',data.columns
    # For each topic id, get all the columns and 
    # concatenate values to form one matrix, then calculate
    # the average
    # There are 50 topics.
    min_final = None
    mean_final = None
    max_final = None

    trecTopics = range(1,51)
    # for tasks track 2015: [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 42, 43, 50]
    for i in trecTopics:
        currQueryDataFrame = None
        for runName, data in dataDict.items():
            try:
                currQueryDataFrame = currQueryDataFrame.append(pd.DataFrame(data[data[u'topic'] == str(i)]))
            except Exception as ex:
                # print 'Error', ex
                currQueryDataFrame = pd.DataFrame(data[data[u'topic'] == str(i)])
        currQueryDataFrame = currQueryDataFrame.drop([u'runid','topic'], axis=1)

        result_min, result_max, result_mean =  pd.DataFrame(currQueryDataFrame.min()),  pd.DataFrame(currQueryDataFrame.max()),pd.DataFrame(currQueryDataFrame.mean())
        result_min.name, result_max.name, result_mean.name = "min", "max", "mean"
        result_min = result_min.transpose()
        result_max = result_max.transpose()
        result_mean = result_mean.transpose()
        result_min['topic'] = i 
        result_max['topic'] = i 
        result_mean['topic'] = i 
        try:
            min_final = min_final.append(result_min)
            mean_final = mean_final.append(result_mean)
            max_final = max_final.append(result_max)
        except:
            min_final = result_min
            max_final = result_max
            mean_final = result_mean
    
    MoveTopicToFront(min_final,'topic').to_csv('min_'+outFile, index=False)
    MoveTopicToFront(mean_final,'topic').to_csv('mean_'+outFile,index=False)
    MoveTopicToFront(max_final,'topic').to_csv('max_'+outFile, index=False)


def MoveTopicToFront(dataframe, colname):
    col = dataframe[colname]
    dataframe=dataframe.drop(colname,axis=1)
    dataframe.insert(0,colname, col)
    return dataframe

def main(argv):
    parser = ap.ArgumentParser(description='Reformat the results to compute min/max/mean of evaluation of all runs.');
    parser.add_argument('-f','--evalFolder', help='Folder containing evaluation of all runs, one per file. \
                                                   The format of such files is : topic number, evalMetric ... ', required=True);
    parser.add_argument('-o','--outFolder', help='File subscript to use when creating files containing \
                                                   min/max/mean of run evaluations ', required=True);
    args = parser.parse_args()
    FindMinMaxAvg(args.evalFolder, args.outFolder)

if __name__ == '__main__':
    main(sys.argv)
