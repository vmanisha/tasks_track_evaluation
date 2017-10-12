import os
import sys

def FindLabelledDocuments(folderName, label_list):
    outF = open('notFoundAdhocDocs.txt','w')

    for fileName in os.listdir(folderName):
        results = {'found':{0:0.0, 1:0.0, 2:0.0, 3:0.0, -2:0.0} , 'notfound':0.0 }
        queryCount = {}
        for line in open(folderName+'/'+fileName,'r'):
            split = line.split(' ')
            docname = split[2] 
            query = split[0]
            if query in ["1","2","3","4","5","6","7","8","9","11","12","14","15","16","17","18","19","20","21","22","23","24","25","26","28","29","31","32","34","35","36","37","42","43","50"]:
                if query not in queryCount: 
                    queryCount[query] =0;
                key = query+'\t'+docname
                if queryCount[query] < 10:
                    if key in  label_list:
                        results['found'][label_list[key]] += 1
                    else:
                        outF.write(line);
                        results['notfound']+= 1
                queryCount[query]+=1

        print fileName, results
    outF.close()



def FindTop10DocumentsPerQuery(foldername):
    topicDocCount = {}
    for filename in os.listdir(foldername):
        queryList = {}
        for line in open(foldername+'/'+filename,'r'):
            split = line.split(' ')
            query = split[0]
            doc = split[2]
            if query in ["1","2","3","4","5","6","7","8","9","11","12","14","15","16","17","18","19","20","21","22","23","24","25","26","28","29","31","32","34","35","36","37","42","43","50"]:
                if query not in queryList:
                    queryList[query] = 0
                if queryList[query] < 10:
                    if query not in topicDocCount:
                        topicDocCount[query] = set()
                    topicDocCount[query].add(doc)
                    queryList[query] +=1
    return topicDocCount


def FindTopicAndDocumentIntersection(topicDocCount1, topicDocCount2):
    for query, docList in topicDocCount1.items():
        #print query, len(docList), len(topicDocCount2[query])
        if query in topicDocCount2:
            print query, len(docList & topicDocCount2[query])




def LoadLabels(fileName):
    label_list = {}
    for line in open(fileName,'r'):
        split = line.split(' ')
        key = split[0]+'\t'+split[2]
        label_list[key] = int(split[-1].strip())

    return label_list

def main(argv):
    # All the adhoc/completion runs need to be in one folder. 
    # argv[1] is the folder with adhoc/completion runs
    # argv[2] is the qrel file
    #label_list = LoadLabels(argv[2])
    #FindLabelledDocuments(argv[1], label_list)
    

    # find the intersection between 2 folder of submitted runs. Top 10 documents are taken for each query from
    # each run in the folder. For each query output the intersection of depth-10 pool of documents between 
    # these two folders.
    # argv[1] = Folder 1 with runs
    # argv[2] = Folder 2 with runs
    topicDocCount1 = FindTop10DocumentsPerQuery(argv[1])
    topicDocCount2 = FindTop10DocumentsPerQuery(argv[2])
    FindTopicAndDocumentIntersection(topicDocCount1, topicDocCount2)



if __name__ == '__main__':
    main(sys.argv)


