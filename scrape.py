from __future__ import division
import traceback
import tabula
import csv
import re
import time
import sys

def format_student(student_details):
    data = '"' + student_details['enrolment_number'] + '","'
    data += student_details['name'] + '","'
    data += student_details['institute'] + '","'
    data += student_details['institute_code'] + '","'
    data += student_details['course'] + '","'
    data += student_details['course_code'] + '","'
    data += student_details['batch'] + '","'
    data += student_details['SID'] + '","'
    data += student_details['schemeID'] + '",'
    return data + '\n'
#----------------------------------------------------------------------
def format_marks(paperid, subject_details, sid, sem):
    mark = subject_details['total']
    if mark != 'A' and mark != 'C' and mark != 'D' and mark != 'RL':
        mark = int(mark.replace("*", ""))
    else:
        mark = 0
    passed = False
    if mark >= int(subject_details['passing_marks']):
        passed = True
    data = 'NULL,"' + paperid + '",'
    data += '"' + sid + '",'
    data += '"' + subject_details['internal'] + '",'
    data += '"' + subject_details['external'] + '",'
    data += '"' + subject_details['total'] + '",'
    if passed:
        data += '"' + subject_details['credits'] + '",'
    else:
        data += '"0",'
    data += '"' + sem + '",'
    if passed:
        data += '1'
    else:
        data += '0'
    return data + '\n'
#----------------------------------------------------------------------
def format_subject(paperid, subject_details,scheme):
    data = '"' + paperid + '",'
    data += '"' + subject_details['code'] + '",'
    data += '"' + subject_details['name'] + '",'
    data += '"' + subject_details['type'] + '",'
    data += '"' + subject_details['credits'] + '",'
    data += '"' + subject_details['passing_marks'] + '",'
    data += '"' + scheme + '"'
    return data + '\n'
#----------------------------------------------------------------------
def get_details(eno):
    data = dict()
    colleges = {
        "964":"MAHARAJA AGRASEN INSTITUTE OF TECHNOLOGY",
        "148":"MAHARAJA AGRASEN INSTITUTE OF TECHNOLOGY",
        "133":"HMR INSTITUTE OF TECHNOLOGY & MANAGEMENT",
        "965":"HMR INSTITUTE OF TECHNOLOGY & MANAGEMENT",
        "768":"GURU TEGH BAHADUR INSTITUTE OF TECHNOLOGY",
        "512":"BHARATI VIDYAPEETH COLLEGE OF ENGINEERING",
        "115":"BHARATI VIDYAPEETH COLLEGE OF ENGINEERING",
        "963":"MAHARAJA SURAJMAL INSTITUTE OF TECHNOLOGY",
        "962":"NORTHERN INDIA ENGINEERING COLLEGE",
        "150":"MAHARAJA SURAJMAL INSTITUTE OF TECHNOLOGY",
        "209":"G B PANT GOVT. ENGINEERING COLLEGE",
        "208":"BHAGWAN PARSHURAM INSTITUTE OF TECHNOLOGY",
        "156":"NORTHERN INDIA ENGINEERING COLLEGE",
        "551":"MAHAVIR SWAMI INSTITUTE OF TECHNOLOGY",
        "701":"ANSAL INSTITUTE OF TECHNOLOGY",
        "132":"GURU TEGH BAHADUR INSTITUTE OF TECHNOLOGY",
        "180":"DELHI TECHNICAL CAMPUS, GREATER NOIDA",
        "135":"INDIRA GANDHI INSTITUTE OF TECHNOLOGY",
        "101":"AMBEDKAR INSTITUTE OF ADVANCED COMMUNICATION TECHNOLOGIES & RESEARCH (FORMERLY AIT)",
        "104":"AMITY SCHOOL OF ENGINEERING & TECHNOLOGY",
        "255":"JIMS ENGINEERING MANAGEMENT TECHNICAL CAMPUS, GREATER NOIDA",
        "702":"DELHI INSTITUTE OF TOOL ENGINEERING",
        "207":"CH. BRAHAM PRAKASH GOVERNMENT ENGINEERING COLLEGE",
        "256":"DELHI TECHNICAL CAMPUS, GREATER NOIDA",
        "153":"NATIONAL POWER TRAINING INSTITUTE",
        "553":"BM INSTITUTE OF ENGINEERING & TECHNOLOGY",
        "552":"BHAGWAN MAHAVEER COLLEGE OF ENGINEERING & MANAGEMENT"
    }
    courses = {
        "027" : "BACHELOR OF TECHNOLOGY (COMPUTER SCIENCE ENGINEERING)",
        "028" : "BACHELOR OF TECHNOLOGY (ELECTRONICS AND COMMUNICATIONS ENGINEERING)",
        "030" : "BACHELOR OF TECHNOLOGY (INSTRUMENTATION AND CONTROL ENGINEERING)",
        "031" : "BACHELOR OF TECHNOLOGY (INFORMATION TECHNOLOGY ENGINEERING)",
        "034" : "BACHELOR OF TECHNOLOGY (CIVIL ENGINEERING)",
        "036" : "BACHELOR OF TECHNOLOGY (MECHANICAL AND AUTOMATION ENGINEERING)",
        "037" : "BACHELOR OF TECHNOLOGY (POWER ENGINEERING)",
        "049" : "BACHELOR OF TECHNOLOGY (ELECTRICAL AND ELECTRONICS ENGINEERING)",
        "056" : "BACHELOR OF TECHNOLOGY (ENVIRONMENTAL ENGINEERING)",
        "086" : "BACHELOR OF TECHNOLOGY (TOOLS ENGINEERING)",
        "110" : "BACHELOR OF TECHNOLOGY (ELECTRICAL ENGINEERING)",
        "111" : "BACHELOR OF TECHNOLOGY (MECHANICAL ENGINEERING)",
        "112" : "BACHELOR OF TECHNOLOGY (MECHATRONICS)",
        "072" : "BACHELOR OF TECHNOLOGY (COMPUTER SCIENCE ENGINEERING)",
        "073" : "BACHELOR OF TECHNOLOGY (ELECTRONICS AND COMMUNICATIONS ENGINEERING)",
        "076" : "BACHELOR OF TECHNOLOGY (INSTRUMENTATION AND CONTROL ENGINEERING)",
        "077" : "BACHELOR OF TECHNOLOGY (INFORMATION TECHNOLOGY ENGINEERING)",
        "079" : "BACHELOR OF TECHNOLOGY (CIVIL ENGINEERING)",
        "074" : "BACHELOR OF TECHNOLOGY (MECHANICAL AND AUTOMATION ENGINEERING)",
        "075" : "BACHELOR OF TECHNOLOGY (POWER ENGINEERING)",
        "078" : "BACHELOR OF TECHNOLOGY (ELECTRICAL AND ELECTRONICS ENGINEERING)",
        "080" : "BACHELOR OF TECHNOLOGY (ENVIRONMENTAL ENGINEERING)",
        "081" : "BACHELOR OF TECHNOLOGY (TOOLS ENGINEERING)",
        "083" : "BACHELOR OF TECHNOLOGY (ELECTRICAL ENGINEERING)",
        "082" : "BACHELOR OF TECHNOLOGY (MECHANICAL ENGINEERING)",
        "084" : "BACHELOR OF TECHNOLOGY (MECHATRONICS)"
    }
    data['institute_code'] = eno[3:6]
    data['institute'] = colleges[eno[3:6]] if eno[3:6] in colleges else "UNKNOWN"
    data['course_code'] = eno[6:9]
    data['course'] = courses[eno[6:9]] if eno[6:9] in courses else "UNKNOWN"
    data['batch'] = '20' + eno[9:11].zfill(2)
    return data
#----------------------------------------------------------------------
def get_subject_data(row):
    data = dict()
    data['code'] = row[1]
    data['name'] = row[2]
    data['credits'] = row[3]
    data['type'] = row[4]
    data['passing_marks'] = row[11]
    return data
#----------------------------------------------------------------------
def csv_reader(file_obj):
    #-------------- FILES ---------------
    studentscsv = open("students.csv", "a")
    subjectscsv = open("subjects.csv", "a")
    markscsv = open("marks.csv", "a")
    #------------------------------------
    i = 0
    subject_details = dict()
    student_details = dict()
    subjects = []
    internal = []
    external = []
    total_marks = []
    reader = csv.reader(file_obj)
    student_details['semester'] = sys.argv[2]
    for index, row in enumerate(reader):
        try:
            i += 1
            if i == 1:
                if len(row[1].replace(' ', '')) == 7:
                    i = 0
                    subject_details[row[0]] = get_subject_data(row)
                else:
                    student_details['enrolment_number'] = row[0]
                    student_details = dict(student_details, **get_details(row[0]))
                    for j in range(1, len(row)-1):
                        if row[j] != '':
                            subject = re.search(r'(.*)\(.*\)', row[j]).group(1)
                            subjects.append(subject)
                    student_details['credits_secured'] = row[len(row)-1]
            elif i == 2:
                student_details['name'] = row[0]
            elif i == 3:
                student_details['SID'] = re.search(r'SID: (.*)', row[0]).group(1)
                for j in range(1, len(row)-1):
                    if row[j] != '':
                        intext = re.search(r'(.*) (.*)', row[j])
                        internal.append(intext.group(1).strip())
                        external.append(intext.group(2).strip())
            elif i == 4:
                if row[0] == "":
                    for j in range(1, len(row)-1):
                        if row[j] != '':
                            intext = re.search(r'(.*) (.*)', row[j])
                            internal.append(intext.group(1))
                            external.append(intext.group(2))
                    i -= 1
                else:
                    student_details['schemeID'] = re.search(r'SchemeID: (.*)', row[0]).group(1)
            elif i == 5:
                for j in range(1, len(row)-1):
                    if row[j] != '':
                        if '(' in row[j]:
                            total_marks.append(re.search(r'(.*)\((.*)\)', row[j]).group(1))
                        else:
                            total_marks.append(row[j])
                i = 0

                data = [{'internal':inter, 'external': ext, 'total': total}
                        for inter, ext, total in zip(internal, external, total_marks)]
                marks = dict(zip(subjects, data))
                for paperid in marks:
                    marks[paperid] = dict(marks[paperid], **subject_details[paperid])
                    subjectscsv.write(format_subject(paperid, subject_details[paperid],
                                                     student_details['schemeID']))
                    markscsv.write(format_marks(paperid, marks[paperid],
                                                student_details['SID'],
                                                student_details['semester']))
                student_details['marks'] = marks
                #------------ FORMATTING DATA ---------------------
                studentscsv.write(format_student(student_details))
                #----------------- MEMORY HANDLING ----------------
                del subjects[:]
                del internal[:]
                del external[:]
                del total_marks[:]
                del subject_details[:]
                del student_details[:]
        except Exception as e:
            if str(e) != "unhashable type":
                print 'Exception @ ' + str(index)
                traceback.print_exc()
                print '\n'
    studentscsv.close()
    subjectscsv.close()
    markscsv.close()
#----------------------------------------------------------------------
if __name__ == "__main__":
    pdf_path = sys.argv[1]
    csv_path = "output.csv"
    t0 = time.time()
    tabula.convert_into(pdf_path, csv_path, output_format='csv', pages='all',
                        area=[197.259375, 26.7975, 739.164375, 1189.51125], guess=False, stream=True)
    with open(csv_path, "rb") as f_obj:
        csv_reader(f_obj)
    t1 = time.time()
    print "PDF processed in {} seconds".format(t1-t0)
