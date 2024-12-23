from telethon import TelegramClient
from data import *

client = TelegramClient('session_file', api_id, api_hash)
client.start()

F = open("list.txt", "w")

result = ""
dialog = client.get_dialogs(limit=None)
for single in dialog:
    result += str(single.name) + '|' + str(single.entity.id) + '\r\n'

F.write(result)
F.close()

