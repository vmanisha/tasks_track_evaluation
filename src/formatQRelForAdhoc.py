import argparse as ap
import sys
def FormatForAdhoc(relFile):
    for line in open(relFile,'r'):
        split = line.strip().split(' ')
        topic = split[0]
        subtopic = int(split[1])
        if subtopic == 1:
            print split[0],0,split[2],split[3]


def FormatForAdhocFindMax(relFile, judgment_index):
    judgmentDict ={}
    for line in open(relFile,'r'):
        split = line.strip().split(' ')
        topic = split[0]
        judgment = int(split[judgment_index])
        document  = split[2]
        if topic not in judgmentDict:
            judgmentDict[topic] = {}
        if document not in judgmentDict[topic]:
            judgmentDict[topic][document] = {}
        if judgment not in judgmentDict[topic][document]:
            judgmentDict[topic][document][judgment] = 0
        judgmentDict[topic][document][judgment] +=1

    for topic, docJudgeDict in judgmentDict.items():
        for doc, judgmentDict in docJudgeDict.items():
            finalJudged = None
            judgSorted = sorted(judgmentDict.items(), reverse = True, key = lambda x : x[1])
            # if 0 is top judgment
            if judgSorted[0][0] == 0:
                if len(judgSorted) == 1:
                    finalJudged = 0
                else:
                    finalJudged = max(judgmentDict.keys()) 
            else:
                finalJudged = judgSorted[0][0]
            if finalJudged != None:
                print topic, 0, doc, finalJudged
            else:
                print 'Not Found', topic, doc, judgSorted


def main(argv):    
    parser = ap.ArgumentParser(description='Reformat diversity based qrel file into adhoc qrel file.');
    parser.add_argument('-q','--qrelFile', help='Qrel file to format into standard TREC adhoc format', required=True);
    parser.add_argument('-j','--judgmentType', help='Tasks track evaluates relevance and usefulness. \
                                                     Current qrel format for task completion is : \n\
						     topic-id subtask-id docno rel-judgment utility-judgment \n\
						     Thus options for judgments is "relevance" or "usefullness".', required=True);
    args = parser.parse_args()
    if args.judgmentType == 'relevance':
	judgment_index = 3
    else:
	judgment_index = 4

    FormatForAdhocFindMax(args.qrelFile, judgment_index)
    
if __name__ == '__main__':
    main(sys.argv)
