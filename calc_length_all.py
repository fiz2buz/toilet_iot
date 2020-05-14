import glob
import csv
from datetime import datetime as dt
import datetime
import matplotlib.pyplot as plt

def calc_total_length(datas):
    return len(datas)/6.3

def calc_ave_speed(datas):
    start_time = dt.strptime(datas[0], "%Y%m%d_%H:%M:%S,%f")
    finish_time = dt.strptime(datas[len(datas)-1], "%Y%m%d_%H:%M:%S,%f")
    return calc_total_length(datas)/(finish_time-start_time).total_seconds()

def calc_how_many_days(file_list):
    # 降順でソート
    file_list.sort()

    start_time = dt.strptime(del_someword(file_list[0], 6, -4), "%Y%m%d_%H%M%S")
    finish_time = dt.strptime(del_someword(file_list[len(file_list)-1], 6, -4), "%Y%m%d_%H%M%S")
    return datetime.timedelta(seconds=(finish_time-start_time).total_seconds()).days

def del_someword(date_str, n, m):
    return date_str[n:m]

file_list = glob.glob("./out/*.csv")

sum = 0
total_days = calc_how_many_days(file_list)

for file in file_list:
    CSV_FILE = open(file, "r", encoding="ms932", errors="", newline="" )
    f = csv.reader(CSV_FILE, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    datas = next(f)
    sum += calc_total_length(datas)

print("> total used lenght of toilet paper :" + str(int(sum)) + " cm")
print("> total days :" + str(total_days))
print("> Average lenght using toilet paper each day: " + str(int(sum/total_days)) + " cm")
