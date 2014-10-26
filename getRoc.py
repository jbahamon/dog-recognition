import numpy as np

#1 : dog
#0 : no dog
def processFile(inFile,thetas):
    #header doesn't help us
    inFile.readline()
    # now read what is important
    total_positives = 0
    total_negatives = 0
    TP = [0.0] * len(thetas)
    FP = [0.0] * len(thetas)
    
    j = 0
    for line in inFile:
        j += 1
        line = line.split();
        # asigned class, class1 prob, class0 prob
        line = [int(line[0]),float(line[1]),float(line[2])]
        
        for i in range(len(thetas)):
            if line[1] > thetas[i]:
                total_positives += 1
            else:
                total_negatives += 1
            # dogP / nodogP
            if line[1] / line[2] > thetas[i]:
                #current_positives += 1
                if j < 200:#is REALLY a dog?
                    TP[i] += 1
                else:
                    FP[i] += 1
        
    TPR = [ positives / total_positives for positives in TP ]
    FPR = [ positives / total_negatives for positives in FP ]
    
    return zip(FPR,TPR)

def writeFile(aList,outfile):
    outfile.write("theta\tFPR\tTPR\n")
    for (theta,(F,T)) in aList:
        outfile.write(str(theta)+'\t'+str(F)+'\t'+str(T)+'\n')

files = [
        "results100",
        "results500",
        "results1000",
        "results1500"
        ]

thetas = np.arange(0.1, 1, 0.05).tolist()

for f in files:
    inF = open(f,'r')
    outF = open("informe/"+f+"-ROC.csv",'w')
    writeFile(zip(thetas,processFile(inF,thetas)),outF)
    outF.close()
    inF.close()

#out = open("rocPoints.csv","w")
#thetas = np.arange(0.1, 0.9, 0.05).tolist()
#out.write(str(["file"]+thetas)+'\n')
#for f in files:
#    inF = open(f,"r")
#    arr = [f] + processFile(inF,thetas)
#    out.write(str(arr)+'\n')
#    inF.close()
#out.close()
