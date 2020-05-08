import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import csv
import collections

def del_someword(date_str):
    return date_str[:-2]

FILE_NAME = "20200506_233732.csv"
CSV_FILE = open("./" + FILE_NAME, "r", encoding="ms932", errors="", newline="" )

f = csv.reader(CSV_FILE, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)


datas = map(del_someword, next(f))

each_time_counts = collections.Counter(datas)

print(each_time_counts)
print("> tyr to sort the list...")

time_list = []
count_list = []

for time in sorted(each_time_counts.keys()):
    time_list.append(datetime.datetime.strptime(time, "%Y%m%d_%H:%M:%S,%f"))
    count_list.append(each_time_counts[time])

for x in range(1, len(count_list)):
    count_list[x] += count_list[x -1]

plt.plot(time_list, count_list)
plt.show()