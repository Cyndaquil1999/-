import os
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

n = 10
#返信機能
if n == 10:
    @app.message("A")
    def say_hello(message, say):
        print(message)
        say(f'<@{message["user"]}> さん、こんにちは！')


@app.message("Hello")
def say_hello(message, say):
    print(message)
    say(f'<@{message["user"]}> さん、こんにちは！')
    
@app.message("time")
def say_nowtime(message, say):
    now = datetime.datetime.now().strftime("%H時%M分%S秒")
    say(now)
    
@app.message("Neity")
def say_neity(message, say):
    say("https://zukan.pokemon.co.jp/zukan-api/up/images/index/c9ab23aadc469d0c3b857d0217e804b3.png")


@app.command("/modal-command")
def handle_some_command(ack: Ack, body: dict, client: WebClient):
    # 受信した旨を 3 秒以内に Slack サーバーに伝えます
    ack()
    # views.open という API を呼び出すことでモーダルを開きます
    client.views_open(
        # 上記で説明した trigger_id で、これは必須項目です
        # この値は、一度のみ 3 秒以内に使うという制約があることに注意してください
        trigger_id=body["trigger_id"],
        # モーダルの内容を view オブジェクトで指定します
        view=
                {"blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with a button."
                        },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click Me"
                    },
                    "value": "click_me_123",
                    "action_id": "button"
                            }
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
        }    
                
    )          
"""
        {
            # このタイプは常に "modal"
            "type": "modal",
            # このモーダルに自分で付けられる ID で、次に説明する @app.view リスナーはこの文字列を指定します
            "callback_id": "modal-id",
            # これは省略できないため、必ず適切なテキストを指定してください
            "title": {"type": "plain_text", "text": "ネイティ"},
            # input ブロックを含まないモーダルの場合は view から削除することをおすすめします
            # このコード例のように input ブロックがあるときは省略できません
            "submit": {"type": "plain_text", "text": "送信"},
            # 閉じるボタンのラベルを調整することができます（必須ではありません）
            "close": {"type": "plain_text", "text": "閉じる"},
            # Block Kit の仕様に準拠したブロックを配列で指定
            # 見た目の調整は https://app.slack.com/block-kit-builder を使うと便利です
            "blocks": [
                {
                    # 様々なブロックのうち input ブロックだけがデータ送信に含まれます
                    # ブロックの一覧はこちら: https://api.slack.com/reference/block-kit/blocks
                    "type": "input",
                    # block_id / action_id を指定しない場合 Slack がランダムに指定します
                    # この例のように明に指定することで、@app.view リスナー側での入力内容の取得で
                    # ブロックの順序に依存しないようにすることをおすすめします
                    "block_id": "question-block",
                    # ブロックエレメントの一覧は https://api.slack.com/reference/block-kit/block-elements
                    # Works with block types で Input がないものは input ブロックに含めることはできません
                    "element": {"type": "plain_text_input", "action_id": "input-element"},
                    # これはモーダル上での見た目を調整するものです
                    # 同様に placeholder を指定することも可能です 
                    "label": {"type": "plain_text", "text": "質問"},
                }
            ],
        },
        
"""


    
#アプリの起動
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    
