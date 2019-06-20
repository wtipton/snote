import json
import requests

import config
from constants import ViewFormat
from view import View
from villain import Villain

class Controller:
  def __init__(self):
    self.cfg = config.Config()
    self.view = View(self.LblLeftClickHandler, self.LblRightClickHandler, self.NotesUpdatedHandler)
    self.view_format = ViewFormat.LABEL_ONLY
    self.view.SetViewFormat(self.view_format)
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
        self.view.SetLabelText('No villain found.')
    except Exception as e:
      self.view.SetLabelText("Can't connect to API.")
      print (e)

  def Run(self):
    self.view.Run()

  # Make us smaller.
  def LblLeftClickHandler(self, e):
    if self.view_format == ViewFormat.TAB:
      pass
    elif self.view_format == ViewFormat.LABEL_ONLY:
      self.view_format = ViewFormat.TAB
    else:
      self.view_format = ViewFormat.LABEL_ONLY
    self.view.SetViewFormat(self.view_format)

  # Make us bigger.
  def LblRightClickHandler(self, e):
    if self.view_format == ViewFormat.TAB:
      self.view_format = ViewFormat.LABEL_ONLY
    elif self.view_format == ViewFormat.LABEL_ONLY:
      self.view_format = ViewFormat.NOTES_VIEW
    self.view.SetViewFormat(self.view_format)

  def NotesUpdatedHandler(self, e):
    self.villain.SaveNotes(self.view.GetVillainNotes())
