from flask import Flask, request
from key import bot_token, bot_user_name, URL
import telegram, requests

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # TODO: do something with the message

    return 'ok'


if __name__ == "__main__":
    app.run(debug=True)
 