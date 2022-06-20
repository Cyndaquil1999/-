import RPi.GPIO as GPIO
import time
import datetime

Numbers = ["0000", "0001", "0010", "0011", "0100",
           "0101", "0110", "0111", "1000", "1001"]

def setup(li: list):
    for number in li:
        GPIO.setup(number, GPIO.OUT, initial=GPIO.HIGH)

#GPIO番号を4つずつ振っておく
Digits = [24, 23, 22, 27] #DIG1, DIG2, DIG3, DIG4
InputD = [20, 26, 21, 16] #D3, D2, D1, D0
SW = 6
SW_flg = 0
t = 0.001

GPIO.setmode(GPIO.BCM)
setup(Digits)
setup(InputD)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def zero_padding(time: str):
    if len(time) == 1:
        time = "0" + time
    
    return time

def turn_on_off(num: str):
    for digit in range(len(num)):
        if num[digit] == "0":
            GPIO.output(InputD[digit], GPIO.LOW)
        else:
            GPIO.output(InputD[digit], GPIO.HIGH)
            

def show_number(number: str):
    for index ,value in enumerate(number):
        #digit on
        GPIO.output(Digits[index], GPIO.LOW)
            
        #turn on
        num = Numbers[int(value)]
        turn_on_off(num)
            
        time.sleep(t)
            
        #turn off
        num = "1010"
        turn_on_off(num)

        #digit off
        GPIO.output(Digits[index], GPIO.HIGH)
            
def checkSW(pin):
    global SW_flg
    
    if SW_flg == 0:
        SW_flg = 1
    else:
        SW_flg = 0
    
    
def change_number(SW_flg: int):
    Now = datetime.datetime.now()
    month = Now.month
    day = Now.day
    hour = Now.hour
    minute = Now.minute
    
    if SW_flg == 0:
        tmp_month = str(month)
        tmp_day = str(day)
        
        tmp_month = zero_padding(tmp_month)
        tmp_day = zero_padding(tmp_day)

        number = tmp_month + tmp_day
        
        show_number(number)

         
    else:
        tmp_hour = str(hour)
        tmp_minute = str(minute)
        
        tmp_hour = zero_padding(tmp_hour)
        tmp_minute = zero_padding(tmp_minute)

        number = tmp_hour + tmp_minute
        show_number(number)

GPIO.add_event_detect(SW, GPIO.FALLING, callback=checkSW, bouncetime=200)

try:
    while True:
        change_number(SW_flg)
        print("SW_flg: {}".format(SW_flg))

except KeyboardInterrupt:
    pass


GPIO.cleanup()
