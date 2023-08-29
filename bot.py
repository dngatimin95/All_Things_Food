import requests
import logging
import telebot
from key import GMAPS_API, BOT_TOKEN

FOOD_URL = "http://0.0.0.0:5000/locus" # https://allthingsfood.onrender.com
GMAPS_URL_FIRST = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=place_id%2Cformatted_address%2Cname%2Ctype%2Curl&input="
GMAPS_URL_SECOND = "&inputtype=textquery&key=" + GMAPS_API

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.


@bot.message_handler(commands=['start', 'hello'])
def start(message):
    kb = telebot.types.InlineKeyboardMarkup()
    msg = "Hello, {}! What can I do for you today? Here are some suggestions:".format(message.from_user.first_name)
  
    kb.row(telebot.types.InlineKeyboardButton('Add Locus', callback_data='add-locus'))
    kb.row(
      telebot.types.InlineKeyboardButton('Get Locus', callback_data='get-locus'),
      telebot.types.InlineKeyboardButton('Get Nearest Locus', callback_data='get-nearest-locus')
    )
    kb.row(
      telebot.types.InlineKeyboardButton('Delete Locus', callback_data='delete-locus'),
      telebot.types.InlineKeyboardButton('Update Locus', callback_data='update-locus')
    )
    bot.send_message(message.chat.id, msg, reply_markup=kb)


@bot.message_handler(commands=['help'])
def help_command(message):
   kb = telebot.types.InlineKeyboardMarkup()
   kb.add(telebot.types.InlineKeyboardButton('Message the developer', url='telegram.me/dngatimin'))
   bot.send_message(
       message.chat.id,
       """1. To add new places, select Add Locus
          \n 2. To get a list of your places, select Get Locus
          \n 3. To get places nearest to you, select Get Nearest Locus
          \n 4. To delete a place, select Delete Locus
          \n 5. To update a place, select Update Locus""",
       reply_markup=kb
   )

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    msg = "Alright, you've selected " + str(query.data)
    data, message = query.data, query.message
    specify_locus(data, message)
    bot.send_message(message.chat.id, msg)

def specify_locus(data, message):
    if data.startswith('add'):
        text = "Please specify the place you want to add and the priority score as well."
        handler = add_locus
    elif data.startswith('get-nearest'):
        text = "Please specify the number of places you want to get and if you want it ranked based on priority score."
        handler = get_nearest_locus
    elif data.startswith('get'):
        text = "Please specify the number of places you want to get and if you want it ranked based on priority score."
        handler = get_locus
    elif data.startswith('delete'):
        text = "Please specify the place you want to delete."
        handler = delete_locus
    elif data.startswith('update'):
        text = "Please specify the place you want to update with the new priority score as well."
        handler = update_locus
    
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, handler)    

# get place details from GMaps API
def get_locus_details(place_name):
    query = place_name.strip().replace(' ', '%20')
    url = GMAPS_URL_FIRST + query + GMAPS_URL_SECOND
    response = requests.get(url).json()
    return response

# add places to allThingsFood API
def add_locus(message):
    place_score = message.text
    place_score_arr = " ".split(place_score.strip())
    place_details = get_locus_details(place_score_arr[0])
    data = place_details["candidates"][0]

    params = {}
    params['priority'] = place_score_arr[1]
    for data_type in data:
        if data_type == "formatted_address":
            params['address'] = data[data_type]
        else:
            params[data_type] = data[data_type]
    
    response = requests.post(FOOD_URL, params)
    bot.send_message(message.chat.id, response.json())
    return response.json()

# get nearest places from allThingsFood API
def get_nearest_locus(message):
    place_amt_rank = message.text
    place_amt_rank_arr = " ".split(place_amt_rank.strip())

    params = {}
    params['amount'] = place_amt_rank_arr[0]
    params['rank_type'] = place_amt_rank_arr[1]
    
    response = requests.get(FOOD_URL, params)
    bot.send_message(message.chat.id, response.json())
    return response.json()

# get places from allThingsFood API
def get_locus(message):
    place_amt_rank = message.text
    place_amt_rank_arr = " ".split(place_amt_rank.strip())

    params = {}
    params['amount'] = place_amt_rank_arr[0]
    params['rank_type'] = place_amt_rank_arr[1]
    
    response = requests.get(FOOD_URL, params)
    bot.send_message(message.chat.id, response.json())
    return response.json()

# delete places from allThingsFood API
def delete_locus(message):
    place = message.text.strip()
    
    DELETE_URL = FOOD_URL + "/" + place

    response = requests.delete(DELETE_URL)
    bot.send_message(message.chat.id, response.json())
    return response.json()

# update places from allThingsFood API
def update_locus(message):
    place_score = message.text
    place_score_arr = " ".split(place_score.strip())
    place_details = get_locus_details(place_score_arr[0])
    data = place_details["candidates"][0]

    params = {}
    params['priority'] = place_score_arr[1]
    for data_type in data:
        if data_type == "formatted_address":
            params['address'] = data[data_type]
        else:
            params[data_type] = data[data_type]
    
    response = requests.put(FOOD_URL, params)
    bot.send_message(message.chat.id, response.json())
    return response.json()

bot.infinity_polling()