import shutil

files = [
        "results100",
        "results500",
        "results1000",
        "results1500"
        ]

for f in files:
    inF = open(f,'r')
    #header don't care
    inF.readline()
    j = 0
    for line in inF:
        # IS dog alg say NO
        if j<200 and int(line[0])==0:
            shutil.copy2("dogs/eval/"+str(j)+".jpg", "isDog/")
        # NOT dog alg say YES
        elif j>200 and int(line[0])==1:
            shutil.copy2("no-dogs/eval/"+str(j-200)+".jpg", "isStuff/")
        j += 1
    inF.close()
