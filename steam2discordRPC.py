#! /bin/env python3

import time
from pypresence import Client
import requests


client_id = '885903500830183475'
steam_id = '196062033'
discord_rpc = Client(client_id)
discord_rpc.start()
discord_rpc.clear_activity()

while True:
  response = requests.post('https://steam-chat.com/miniprofile/' + steam_id + '/json/')
  try:
    print(response.json()["in_game"])
    state = response.json()["in_game"]["rich_presence"]
    if state == "": state = "Playing a game"
    discord_rpc.set_activity(
      state = state,
      large_image = response.json()["in_game"]["logo"],
      details = response.json()["in_game"]["name"]
    )
    time.sleep(30)
  except KeyError:
    discord_rpc.clear_activity()
    time.sleep(120)
