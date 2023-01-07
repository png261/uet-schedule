import requests
import json
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from utils import periodToTime, tableToData

URL_STUDENT_SUBJECTS = "http://112.137.129.87/qldt/?SinhvienLmh%5BmasvTitle%5D={:s}&SinhvienLmh%5BhotenTitle%5D=&SinhvienLmh%5BngaysinhTitle%5D=&SinhvienLmh%5BlopkhoahocTitle%5D=&SinhvienLmh%5BtenlopmonhocTitle%5D=&SinhvienLmh%5BtenmonhocTitle%5D=&SinhvienLmh%5Bnhom%5D=&SinhvienLmh%5BsotinchiTitle%5D=&SinhvienLmh%5Bghichu%5D=&SinhvienLmh%5Bterm_id%5D=036&SinhvienLmh_page=1&ajax=sinhvien-lmh-grid&fbclid=IwAR02TBvY0hrWOP0hkZ2NmZz-YcYLIBWyAMSBrBa-aCnC2kucLIbvkphYfzA"
URL_allSubjects = "http://112.137.129.115/tkb/listbylist.php"

def getSubject(studentID):
    r = requests.get(URL_STUDENT_SUBJECTS.format(studentID))
    table = BeautifulSoup(r.content, 'html.parser').find('table', class_='items') 
    return tableToData(table)


def getAllSubjects():
    subject_infos = BeautifulSoup(requests.get(URL_allSubjects).content, 'html.parser').find_all('table')[3]
    headers = {}
    thead = subject_infos.find("tr").find_all("th")
    if thead:
        for i in range(len(thead)):
            if thead[i].find('option'):
                headers[i] = thead[i].find('option').text
            else:
                headers[i] = thead[i].text
            headers[i] = headers[i].strip().lower()

    return tableToData(subject_infos, headers)


def getSubjectInfo(subjectID, groupID, allSubjects):
    subjectID = ' '.join(subjectID.split(' ')[0:2]) 
    for subject in allSubjects:
        if subject['mã lớp mh'] == subjectID and subject['ghi chú'] == groupID:
            return subject


def showTable(subjects, allSubjects):
    table = PrettyTable(['Mã', 'Tên', 'Thứ', 'Tiết', 'Giảng Đường'])
    table.sortby = "Thứ"
    table.align = 'l'

    for subject in subjects:
        subject_info = getSubjectInfo(subject['mã lmh'], subject['nhóm'], allSubjects)
        if not subject_info:
            table.add_row([subject['mã lmh'],'X', 'X', 'X', 'X'])
            continue
        name = subject_info['tên môn học']
        time = periodToTime(subject_info['tiết'])
        start_time = time['start']
        end_time = time['end']
        weekend = subject_info['thứ']
        place = subject_info['giảng đường']
        table.add_row([subject['mã lmh'], name, weekend, f"{start_time}->{end_time}", place])

    student_name = subjects[0]['họ và tên']
    print(f'Tên sinh viên: {student_name}')
    print(table)


def run():
    studentID = input("Nhập mã sinh viên: ")
    subjects = getSubject(studentID)
    subjects.pop(0)

    showTable(subjects, getAllSubjects())


run()





