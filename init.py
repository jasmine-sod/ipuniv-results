import os
import time
import sys

if len(sys.argv) > 1:
    if sys.argv[1]=='clean':
        os.system('rm *.csv')
        print '%--- CSV FILES CLEANED SUCCESSFULLY ---%\n\n'

os.system('ls Results')

folder = raw_input('Enter folder name: ')

t0 = time.time()
path = 'Results/'+folder+'/'
semesters = os.listdir(path)
if '.DS_Store' in semesters:
    semesters.remove('.DS_Store')
for semester in semesters:
    folder = os.listdir(path + '/' + semester)
    if '.DS_Store' in folder:
        folder.remove('.DS_Store')
    # print folder
    for pdf_file in folder:
        print "Processing " + pdf_file + '\tSEMESTER: ' + semester
        command = 'python scrape.py ' + path + '/' + semester + '/' + pdf_file + ' ' + semester
        os.system(command)
        print '\n'
t1 = time.time()
print "Results processed in {} seconds".format(t1-t0)
os.system('rm output.csv')