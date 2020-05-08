#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO_RPi

# GPIO pin assign
SW_ENCA  = 22
SW_ENCB  = 23

last_encoded = 0
rotate_value = 0
 
last_rotate_value = 0
rotate_value_temp = 0
last_use = 0
stop_count = 0


def setup():
    print("> Start setup...")

    GPIO_RPi.setwarnings(False)
    GPIO_RPi.setmode(GPIO_RPi.BCM)

    # GPIO initialize
    GPIO_RPi.setup(SW_ENCA, GPIO_RPi.IN, pull_up_down=GPIO_RPi.PUD_UP)
    GPIO_RPi.setup(SW_ENCB, GPIO_RPi.IN, pull_up_down=GPIO_RPi.PUD_UP)
    GPIO_RPi.add_event_detect(SW_ENCA, GPIO_RPi.BOTH, callback=callback, bouncetime=5)
    GPIO_RPi.add_event_detect(SW_ENCB, GPIO_RPi.BOTH, callback=callback, bouncetime=5)

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
    condition_list_add_encoderVal=[0b1101, 0b0100, 0b0010, 0b1011]
    condition_list_sub_encoderVal=[0b1110, 0b0111, 0b0001, 0b1000]
    
    global rotate_value
    if state_chenge in condition_list_add_encoderVal:
        rotate_value += 1
    
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
            print("> use_toilet_length: " + str(use_toilet_length))

            if use_toilet_length > 5:
                global rotate_value_temp
                if rotate_value == rotate_value_temp:
                    global stop_count
                    stop_count += 1
                    print("> Stop count : " + str(stop_count))

                    if stop_count > 20:
                        print("おしりを拭きました(´ε｀；)ﾌｷﾌｷ 長さ" + str((rotate_value - last_use)/6.3) + "cm")
                        last_use = rotate_value
                        stop_count = 0
               
                rotate_value_temp = rotate_value
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("break")
        GPIO_RPi.cleanup()

if __name__ == "__main__":
    main()