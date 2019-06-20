import json
import requests

import config
from view import View
from villain import Villain


class Controller:
  def __init__(self):
    self.cfg = config.Config()
    self.view = View(self.LblClickHandler, self.NotesUpdatedHandler)
    self.toggle = False
    self.view.ResizeWindow(False)
    self.villain = Villain('bob', self.cfg.data_dir)
    self.view.AddTask(self.PollAndUpdate, 1000)

  # client api:
  # https://us.battle.net/forums/en/sc2/topic/20748195420
  def PollAndUpdate(self):
    try:
      response = requests.get("http://localhost:6119/game")
      game_info = json.loads(response.text)
      for player in game_info['players']:
        name = player['name']
        if name == self.villain.name:
          break
        elif name != self.cfg.hero:
          self.villain = Villain(name, self.cfg.data_dir)
          self.view.SetLabelText(name)
          self.view.SetNotesText(self.villain.GetNotes())
          break
      else:
        print('couldnt identify villain in api output')
    except Exception as e:
      print ('couldnt open game api: ', e)

  def Run(self):
    self.view.Run()

  def LblClickHandler(self, e):
    self.toggle = not self.toggle
    self.view.ResizeWindow(self.toggle)

  def NotesUpdatedHandler(self, e):
    print(self.view.GetVillainNotes())
    self.villain.SaveNotes(self.view.GetVillainNotes())
