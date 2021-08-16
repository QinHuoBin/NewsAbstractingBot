from pyrogram import Client, filters
from pyrogram.errors.exceptions.flood_420 import FloodWait
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

# app = Client("my_account", api_id, api_hash, proxy={'hostname':'127.0.0.1', 'port':7890})
app = Client("my_account", config_file='my_configuration.ini')

import time

with app:
    # 1627037041
    f = open('time_last_get.txt', 'r')
    time_last_get = int(f.read())
    f.close()

    # 从新到老获取消息
    time_should_get_to = time_last_get
    time_now = int(time.time())
    time_getting = time_now
    message_to_handle = []

    how_many_message_got = 0
    while not time_getting < time_should_get_to:
        a = app.get_history(-1001319457263, offset=how_many_message_got)
        for b in a:
            time_getting = b.date
            if time_getting < time_should_get_to:
                break
            message_to_handle.append([b.text, b.message_id, b.date])
            how_many_message_got += 1
    message_to_handle.reverse()
    print(message_to_handle)

    message_to_send = []
    for message, id, date in message_to_handle:
        first_line = message.splitlines()[0]
        message_to_send.append([first_line, id, date])
    print(message_to_send)
    print('共有{}条消息'.format(len(message_to_send)))

    count = 0
    for message, id, date in message_to_send:
        while True:
            try:
                app.send_message(-1001507308710, message + '\nhttps://t.me/cnbeta_com/{}'.format(id),
                                 disable_web_page_preview=True)
                count += 1
                break
            except FloodWait as e:
                print('消息发送过快，服务器要求睡眠{}秒'.format(e.x))
                print(e)
                print('已发送{}条消息，共有{}条'.format(count, len(message_to_send)))
                print('正在睡眠...')
                time.sleep(int(e.x))
        f = open('time_last_get.txt', 'w')
        f.write(str(date))
        f.close()

    f = open('time_last_finished.txt', 'w')
    f.write(str(time_now))
    f.close()
# 获取所有对话
# with app:
#     for dialog in app.iter_dialogs():
#         #print(dialog.chat.title or dialog.chat.id)
#         print(dialog)
#   pass
# app=Client("my_account", api_id, api_hash, proxy={'hostname':'127.0.0.1', 'port':7890})
#
# # filters.chat("无情的新闻摘要频道")
# @app.on_message(filters.chat(-1001507308710))
# def from_pyrogramchat(client, message):
#     print(message)
#     pass
#
# app.run()
