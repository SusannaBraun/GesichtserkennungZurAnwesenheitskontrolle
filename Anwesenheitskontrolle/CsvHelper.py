import os
from datetime import datetime

def markAttendance(new_name, file_name, path):
    with open(os.path.join(path, file_name), 'r+') as f:
        myDataList = f.readlines()
        print(myDataList)
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if new_name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            dateString = now.strftime('%m:%d:%y')
            f.writelines(f'\n{new_name},{dtString},{dateString}')
        return nameList

