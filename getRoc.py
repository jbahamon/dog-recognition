import numpy as np

def processFile(inFile,thetas):
    #header doesn't help us
    inFile.readline()
    # now read what is important
    
    # positive number: number of images in the dataset that ARE dogs
    P = 200
    # negative number: number of images in the dataset that ARE NOT dogs
    N = 200
    # false positive: number of images that the MODEL SAYS ARE DOGS, but THEY ARE NOT
    FP = [0.0] * len(thetas)
    # true positive: number of images that the MODEL SAYS ARE DOGS, and THLEY ARE 
    TP = [0.0] * len(thetas)
    
    #image counter - over 200 are no-dogs
    j = 0
    for line in inFile:
        line = line.split();
        
        #1 : dog
        #0 : no dog
        given_class = int(line[0])
        dog_P = float(line[1])
        nodog_P = float(line[2])
        
        # model says is a dog
        for i in range(len(thetas)):
            if dog_P / nodog_P > thetas[i]:
                if j < 200:#is REALLY a dog?
                    TP[i] += 1
                else:
                    FP[i] += 1
        j += 1
    TPR = [ positives / P for positives in TP ]
    FPR = [ positives / N for positives in FP ]
    
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
