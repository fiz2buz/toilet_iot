import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
import matplotlib.dates as mdates
import csv
import collections
import glob
import copy as cp

file_list = glob.glob("./out/*.csv")

time_format = "%Y%m%d_%H:%M:%S,%f"

def del_someword(date_str):
    return date_str[:-2]

for file in file_list:
    CSV_FILE = open(file, "r", encoding="ms932", errors="", newline="" )
    f = csv.reader(CSV_FILE, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    
    data_list = next(f)

    list_copy = cp.copy(data_list)
    start_time = dt.strptime(del_someword(list_copy[0]), time_format)
    
    datas = map(del_someword,data_list)

    each_time_counts = collections.Counter(datas)

    time_list = []
    length_list = []

    for time in sorted(each_time_counts.keys()):
        time_list.append( (dt.strptime(time, time_format) - start_time).total_seconds() )
        length_list.append(each_time_counts[time]/6.3)

    for x in range(1, len(length_list)):
         length_list[x] += length_list[x -1]

    plt.plot(time_list, length_list)
    plt.savefig("out/fig/change_speed/" + file[6:-3] + "png")

    plt.clf()