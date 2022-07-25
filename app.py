import os
import re
from dotenv import load_dotenv
from slack_bolt import App, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
import datetime
import logging
import datetime


load_dotenv()


#アプリの初期化
app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.message("Hello")
def say_hello(message, say):
    print(message)
    say(f'<@{message["user"]}> さん、こんにちは！')
    
@app.message("time")
def say_nowtime(message, say):
    now = datetime.datetime.now().strftime("%H時%M分%S秒")
    say(now)
    

@app.command("/temp")
def handle_some_command(ack: Ack, body: dict, client: WebClient):
    print(body)
    # 受信した旨を 3 秒以内に Slack サーバーに伝えます
    ack()
    # views.open という API を呼び出すことでモーダルを開きます
    client.views_open(
        # 上記で説明した trigger_id で、これは必須項目です
        # この値は、一度のみ 3 秒以内に使うという制約があることに注意してください

        trigger_id=body["trigger_id"],
        # モーダルの内容を view オブジェクトで指定します
        view=
        {
            # このタイプは常に "modal"
            "type": "modal",
            # このモーダルに自分で付けられる ID で、次に説明する @app.view リスナーはこの文字列を指定します
            "callback_id": "modal-id",
            # これは省略できないため、必ず適切なテキストを指定してください
            "title": {"type": "plain_text", "text": "テスト"},
            # input ブロックを含まないモーダルの場合は view から削除することをおすすめします
            # このコード例のように input ブロックがあるときは省略できません
            #"submit": {"type": "plain_text", "text": "送信"},
            # 閉じるボタンのラベルを調整することができます（必須ではありません）
            #"close": {"type": "plain_text", "text": "閉じる"},
            # Block Kit の仕様に準拠したブロックを配列で指定
            # 見た目の調整は https://app.slack.com/block-kit-builder を使うと便利です
            "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This is a section block with a button."
                        },

                    },
                    {
                        "type": "actions",
                        "block_id": "actionblock789",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Primary Button"
                                },
                                "style": "primary",
                                "value": "click_me_456"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Link Button"
                                },
                                "url": "https://api.slack.com/block-kit"
                            }
                        ]
                    }
                ]
        },
    )


    
#アプリの起動
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    
