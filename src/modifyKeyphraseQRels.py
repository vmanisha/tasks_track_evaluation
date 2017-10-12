import argparse as ap
import os
import re
# Given a keyword relevance judgment file and folder of runs, 
# recompute the runs in trec format with each keyword mapped 
# to a unique document id. 
# For Qrels, use the above generated id, and output reformatted 
# qrel. (case is preserved in each file).
# This is to help run Trec eval on these files :D

KEYWORD_STR = 'KEYWORD'
# Returns keyword to file mapping dictionary and writes the TREC
# formated files to the output folder.
def FormatRunFolder(inputRunFolder, outputRunFolder):

    # Standard TREC run file has following format:
    # 0  Q0  ZF08-175-870  0   4238   prise1 
    #qid iter   docno      rank  sim   run_id
    # Keyword run file submitted by participants has format:
    # TOPIC-ID   RANK    SCORE   RUN-ID  KEY-PHRASE

    if not os.path.exists(outputRunFolder):
        os.mkdir(outputRunFolder)
    # Stores keyword -> id mapping
    returnKeywordDict = {}
    # To generate id
    currDocCount=0
    for ifile in os.listdir(inputRunFolder):
        # Topic-Document dictionary, if a document has been covered for
        # a topic dont write it to file.
        topicDocCovered = {}
        ofile = open(outputRunFolder+'/'+ifile,'w')
        for line in open(inputRunFolder+'/'+ifile,'r'):
            # Some teams have both tabs and spaces.
            split = re.split('\s+',line)
            topicId = split[0]
            keyword = ' '.join(split[4:]).strip()
            if keyword not in returnKeywordDict:
                returnKeywordDict[keyword] = KEYWORD_STR+'-'+str(currDocCount)
                currDocCount+=1
            key = topicId+'\t'+returnKeywordDict[keyword]
            if key not in topicDocCovered:
                ofile.write(topicId+' Q0 '+returnKeywordDict[keyword]+' '+' '.join(split[1:4])+'\n')
                topicDocCovered[key] = 1

        ofile.close()
    return returnKeywordDict



def FormatQRelFile(keywordDict, inputFile, outputFile):
    # Format of QRel file: (suitable to run with ndeval)
    # qid subtopic docno rel 
    # NIST submitted format
    # topic-id subtask-id judgment key-phrase 

    ofile = open(outputFile,'w');
    for line in open(inputFile,'r'):
        split = line.split(' ')
        keyword = ' '.join(split[3:]).strip()
        ofile.write(' '.join(split[0:2]) +' '+keywordDict[keyword]+' '+split[2]+'\n')
    ofile.close()



def main():
    parser = ap.ArgumentParser(description='File to re-format keywords qrels and submitted runs given in a folder');
    parser.add_argument('-q','--qrelFile', help='Qrel file to format into standard TREC eval format', required=True);
    parser.add_argument('-s','--runFolder', help='Folder with submitted runs mofified to standard TREC eval format', required=True);
    parser.add_argument('-f','--outputQRelFile', help='File to write modified TREC formatted Qrel', required=True);
    parser.add_argument('-F','--outputRunFolder', help='Folder to write TREC formatted runs', required=True);

    args = parser.parse_args()
    # For each unseen keyword assign a document id and write them to output folder.
    keywordDocumentDict = FormatRunFolder(args.runFolder, args.outputRunFolder)

    # Use the above document ids to regenerate the QRel file.
    FormatQRelFile(keywordDocumentDict, args.qrelFile, args.outputQRelFile)

if __name__ == '__main__':
    main()
