import os
import re
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import datetime

flg = 0

load_dotenv()
#アプリの初期化
app = App(token=os.environ["SLACK_BOT_TOKEN"])

print(flg)

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
    say("28℃です")   


#エアコンの制御を行う
@app.message("エアコン")
def air(message, say):
    global flg
    if flg % 2 == 0:
        say("エアコンが点きました")
        
    else:
        say("エアコンを消しました")
    
    flg += 1


"""
if (flg % 2) == 0:    
    print("flg: {} TorF: {}".format(flg, flg % 2 == 0))
    @app.message(re.compile("エアコンを点けたい"))
    def air_conditioner_on(message, say):
        global flg
        print(flg)
        flg = (flg + 1) % 2
        say("エアコンが付きました")

#エアコンを消す
if (flg % 2) == 1:
    print("flg: {} TorF: {}".format(flg, flg % 2 == 1))
    @app.message(re.compile("エアコンを消したい"))
    def air_conditioner_off(message, say):
        global flg
        print(flg)        
        flg = (flg + 1) % 2
        say("エアコンを消しました")
    
"""
    
#アプリの起動
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    
