import csv
import traceback
csv_path = "marks.csv"

def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    i=1
    for index, row in enumerate(reader):
        try:
            if len(row[2]) > 15:
                print str(i)+" * ERROR in line "+str(index)+"\t\t"+row[2]
                i+=1

        except Exception as e:
            if str(e) != "unhashable type":
                print 'Exception @ ' + str(index)
                traceback.print_exc()
                print '\n'

with open(csv_path, "rb") as f_obj:
        csv_reader(f_obj)
