# インポートするライブラリ
from flask import Flask, request, abort
from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   SourceUser,FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import os
import requests
import urllib.request
import base64

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)
#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
   # get X-Line-Signature header value
   signature = request.headers['X-Line-Signature']
   # get request body as text
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)
   # handle webhook body
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return 'OK'


# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if isinstance(event.source, SourceUser):

        profile = line_bot_api.get_profile(event.source.user_id)

        user_id = profile.user_id

        userid_list = ["id","id","id","id","id"]

        open_key_words = ["開けて","開ける","開","open","開け","開く","解除","あ"]

        close_key_words = ["閉めて","閉める","閉","close","閉じろ","閉まる","施錠","し"]

        def open_close(open_or_close):
            # 送信先のURL
            url = 'url'.format(open_or_close)
            # Basic認証の情報
            user = 'username'
            password = 'pass'
            # Basic認証用の文字列を作成.
            basic_user_and_pasword = base64.b64encode('{}:{}'.format(user, password).encode('utf-8'))
            # Basic認証付きの、GETリクエストを作成する.
            request = urllib.request.Request(url, 
                headers={"Authorization": "Basic " + basic_user_and_pasword.decode('utf-8')})
            # 送信して、レスポンスを受け取る.
            with urllib.request.urlopen(request) as res:
                data = res.read()

            if open_or_close == "open":
                send_message("鍵を解除しました")
            elif open_or_close == "close":
                send_message("鍵を施錠しました")
            else:
                send_message("error")

        def send_message(message):
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
                    )

        if user_id in userid_list:

            text = event.message.text

            if text == 'profile':
                if isinstance(event.source, SourceUser):
                    profile = line_bot_api.get_profile(event.source.user_id)
                    userid = profile.user_id
                    if userid == "id":
                        send_message("")

                    elif userid == "id":
                        send_message("")

                    elif userid == "id":
                        send_message("")

                    elif userid == "id":
                        send_message("")

                    elif userid == "id":
                        send_message("")

                    else:
                        send_message("登録されてません")
            

            elif text in open_key_words:
                open_close("open")

            elif text in close_key_words:
                open_close("close")

            else:
                send_message("無効なコマンドです\n< あける or あけて> → ドアが開きます\n< しめて or しめる> → ドアが閉まります。")

        else:
            send_message("家族以外のメッセージは受け付けません")


if __name__ == "__main__":
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)