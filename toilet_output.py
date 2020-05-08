#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import RPi.GPIO as GPIO_RPi
import csv
import os
import logging

import logging
from _stat import filemode
MYFORMAT='[%(asctime)s]%(filename)s(%(lineno)d): %(message)s'
logging.basicConfig(filename=str('/home/pi/work/out/log/' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.log'),
    filemode='w', # Default is 'a'
    format=MYFORMAT, 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.INFO)

# GPIO pin assign
SW_ENCA  = 22
SW_ENCB  = 23

last_encoded = 0
rotate_value = 0
 
last_rotate_value = 0
rotate_value_temp = 0
last_use = 0
stop_count = 0
toilet_use_list = []

def export_list_csv(export_list, csv_dir):

    with open(csv_dir, "w") as f:
        writer = csv.writer(f, lineterminator='\n')

        if isinstance(export_list[0], list): #多次元の場合
            writer.writerows(export_list)

        else:
            writer.writerow(export_list)

def setup():
    logging.info("> Start setup...")
    print("> Start setup...")
    GPIO_RPi.setwarnings(False)
    GPIO_RPi.setmode(GPIO_RPi.BCM)

    # GPIO initialize
    GPIO_RPi.setup(SW_ENCA, GPIO_RPi.IN, pull_up_down=GPIO_RPi.PUD_UP)
    GPIO_RPi.setup(SW_ENCB, GPIO_RPi.IN, pull_up_down=GPIO_RPi.PUD_UP)
    GPIO_RPi.add_event_detect(SW_ENCA, GPIO_RPi.BOTH, callback=callback, bouncetime=5)
    GPIO_RPi.add_event_detect(SW_ENCB, GPIO_RPi.BOTH, callback=callback, bouncetime=5)

    logging.info("> Finish setup...")
    print("> Finish setup...")
 
def updateEncoder():
    MSB = GPIO_RPi.input(SW_ENCA)
    LSB = GPIO_RPi.input(SW_ENCB)
	
    # A相，B相の入力値を10進数に変換
    encoded = (MSB << 1) | LSB
    
    # 時計回りか反時計回りかを判断するために，前と今の状態変化を計算
    global last_encoded
    state_chenge = (last_encoded << 2) | encoded

	# 加算条件：[13, 4, 2, 11]
	# 減算条件：[14, 7, 1, 8]
    condition_list_sub_encoderVal=[0b1101, 0b0100, 0b0010, 0b1011]
    condition_list_add_encoderVal=[0b1110, 0b0111, 0b0001, 0b1000]
    
    global rotate_value
    if state_chenge in condition_list_add_encoderVal:
        rotate_value += 1
        global toilet_use_list
        now = datetime.datetime.now()
        mmsec = "{0:03d}".format(int(int(now.strftime("%f"))/1000))
        time = str(now.strftime('%Y%m%d_%H:%M:%S,'))
        toilet_use_list.append(time + mmsec)
        print(toilet_use_list)
    
    if state_chenge in condition_list_sub_encoderVal:
        rotate_value -= 1

    last_encoded = encoded
    
def callback(callback):
    updateEncoder()

def main():

    setup()

    try:
        while(True):
            global last_use
            global rotate_value
            use_toilet_length = rotate_value - last_use
            logging.info("> use_toilet_length: " + str(use_toilet_length))
            print("> use_toilet_length: " + str(use_toilet_length))

            if use_toilet_length > 5:
                global rotate_value_temp
                if rotate_value == rotate_value_temp:
                    global stop_count
                    stop_count += 1
                    logging.info("> Stop count : " + str(stop_count))
                    print("> Stop count : " + str(stop_count))

                    if stop_count > 100:
                        logging.info("おしりを拭きました(´ε｀；)ﾌｷﾌｷ 長さ" + str((rotate_value - last_use)/6.3) + "cm")
                        print("おしりを拭きました(´ε｀；)ﾌｷﾌｷ 長さ" + str((rotate_value - last_use)/6.3) + "cm")

                        last_use = rotate_value

                        global toilet_use_list
                        file_path =  "/home/pi/work/out/"
                        file_name = str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')) + ".csv"

                        export_list_csv(toilet_use_list, file_path + file_name)
                        toilet_use_list = []
                        stop_count = 0
               
                rotate_value_temp = rotate_value
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("> break...")
        logging.info("break")
        GPIO_RPi.cleanup()

if __name__ == "__main__":
    main()