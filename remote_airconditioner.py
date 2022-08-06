import os
import re
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import datetime
import smbus
import time
import RPi.GPIO as GPIO
import subprocess


"""
エアコン制御周り
"""
flg = 0



"""
温度センサ周り
"""
i2c = smbus.SMBus(1)
address = 0x48

def read_adt7410():
    byte_data = i2c.read_byte_data(address, 0x00)
    data = byte_data << 5
    byte_data = i2c.read_byte_data(address, 0x01)
    data = data + (byte_data >> 3)
    data = data * 0.0625
    return data

"""
7segLED周り
"""

#7セグLEDの処理
Numbers =  ["0000", "0001", "0010", "0011", "0100",
           "0101", "0110", "0111", "1000", "1001"]

def setup(li: list):
    for number in li:
        GPIO.setup(number, GPIO.OUT, initial=GPIO.HIGH)

#GPIO番号で書いています
Digits = [22, 27] #DIG3, DIG4
InputD = [20, 26, 21, 16] #D3, D2, D1, D0
delay_time = 0.001

GPIO.setmode(GPIO.BCM)
setup(Digits)
setup(InputD)

def turn_on_off(num: str):
    for digit in range(len(num)):
        if num[digit] == "0":
            GPIO.output(InputD[digit], GPIO.LOW)
        else:
            GPIO.output(InputD[digit], GPIO.HIGH)

def show_temperture(number: str):
    for idx, val in enumerate(number):
        #桁の選択
        GPIO.output(Digits[idx], GPIO.LOW)

        #LEDを点灯させる
        num = Numbers[int(val)]
        #print("num: {}".format(num))
        turn_on_off(num)

        #${delay_time}(sec)だけ待機する
        time.sleep(delay_time)

        #LEDを消灯させる
        num = "1010"
        turn_on_off(num)

        #桁の選択を解除する
        GPIO.output(Digits[idx], GPIO.HIGH)



load_dotenv()
#アプリの初期化
app = App(token=os.environ["SLACK_BOT_TOKEN"])


#動作確認用
@app.message("Hello")
def say_hello(message, say):
    print(message)
    say(f'<@{message["user"]}> さん、こんにちは！')
    
#時間を返す
@app.message("time")
def say_nowtime(message, say):
    now = datetime.datetime.now().strftime("%H時%M分%S秒")
    say(now)
    
#温度を返す
@app.message(re.compile("temperture|温度"))
def say_temperture(message, say):
    tmp = str(format(read_adt7410(), ".0f"))
    say("{}℃です".format(tmp))   
    st = time.time()
    
    #LED test
    #tmp = ""
    
    while True:
        show_temperture(tmp)
        if time.time() - st >= 15:
            break
    

#エアコンの制御を行う
@app.message("エアコン")
def air(message, say):
    global flg
    if flg % 2 == 0:
        
        subprocess.run(["python3", "irrp.py", "-p", "-g6", "-f", "power_on", "power:on"])
        say("エアコンが点きました")
        
    else:
        subprocess.run(["python3", "irrp.py", "-p", "-g6", "-f", "power_down", "power:down"])
        say("エアコンを消しました")
    
    flg += 1
    
 
#アプリの起動
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


GPIO.cleanup()