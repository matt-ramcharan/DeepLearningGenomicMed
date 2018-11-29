import csv
import os
import itertools

#relative = "../"
#print(os.path.abspath(relative))
#print(os.path.exists("/home/matt/Documents/TechnicalProject/Data/CosmicCompleteTargetedScreensMutantExport.tsv"))


with open('/home/matt/Documents/TechnicalProject/Data/CosmicCompleteTargetedScreensMutantExport.tsv','rt') as tsvin, open('/home/matt/Documents/TechnicalProject/Data/new.csv', 'wt') as csvout, open('/home/matt/Documents/TechnicalProject/Data/new.csv', 'rt') as csvread:
    tsvin = csv.reader(tsvin, delimiter='\t')
    csvout = csv.writer(csvout)
    csvread = csv.reader(csvread)

    for row in tsvin:
        if row[29] != "":
            csvout.writerows([row])

        row_count = sum(1 for row in csvread)
        if row_count>500:
            break

    Status = []
    for row in csvread:
        if row[29] not in Status:
            Status.append(row[29])
    print(Status)