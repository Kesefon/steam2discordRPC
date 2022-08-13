#! /bin/env python3

import time
from pypresence import Client
import requests

client_id = '1007823600230879272'
steam_id = '196062033'
blacklist = ['945360']

discord_rpc = Client(client_id)
while True:
  try:
    discord_rpc.start()
    break
  except ConnectionRefusedError:
    time.sleep(5*60)
discord_rpc.clear_activity()

while True:
  response = requests.post('https://steam-chat.com/miniprofile/' + steam_id + '/json/')
  try:
    print(response.json()["in_game"])
    appid = response.json()["in_game"]["logo"][46:-19]
    if appid in blacklist:
      discord_rpc.clear_activity()
      time.sleep(120)
    else:
      print(appid) #TODO: appid based override
      state = response.json()["in_game"]["rich_presence"]
      if state == "": state = None
      discord_rpc.set_activity(
        state = state,
        large_image = response.json()["in_game"]["logo"],
        details = response.json()["in_game"]["name"],
        buttons = [{"label": "Open Store Page", "url": "https://store.steampowered.com/app/" + appid}, {"label": "Launch Game", "url": "steam://run/" + appid}]
      )
      time.sleep(30)
  except KeyError:
    discord_rpc.clear_activity()
    time.sleep(120)
