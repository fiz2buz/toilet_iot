import glob
import csv
from datetime import datetime as dt
import matplotlib.pyplot as plt

def calc_total_length(datas):
    return len(datas)/6.3

def calc_ave_speed(datas):
    start_time = dt.strptime(datas[0], "%Y%m%d_%H:%M:%S,%f")
    finish_time = dt.strptime(datas[len(datas)-1], "%Y%m%d_%H:%M:%S,%f")
    return calc_total_length(datas)/(finish_time-start_time).total_seconds()


file_list = glob.glob("./out/*.csv")

length_list = []
speed_list = []

for file in file_list:
    CSV_FILE = open(file, "r", encoding="ms932", errors="", newline="" )
    f = csv.reader(CSV_FILE, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    datas = next(f)
    length_list.append(calc_total_length(datas))
    speed_list.append(calc_ave_speed(datas))
    print("速度：" + str(calc_ave_speed(datas)) + "\n長さ：" + str(calc_total_length(datas)))

plt.scatter(length_list, speed_list)
plt.show()



# print(each_time_counts)
# print("> tyr to sort the list...")

# time_list = []
# count_list = []

# for time in sorted(each_time_counts.keys()):
#     time_list.append(datetime.datetime.strptime(time, "%Y%m%d_%H:%M:%S,%f"))
#     count_list.append(each_time_counts[time])

# for x in range(1, len(count_list)):
#     count_list[x] += count_list[x -1]

# plt.plot(time_list, count_list)
# plt.show()