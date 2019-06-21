import json
import requests

from build import Build
import config
from constants import ViewFormat
from view import View
from villain import Villain

class Controller:
  def __init__(self):
    self.cfg = config.Config()
    self.view = View(self.LblLeftClickHandler, self.LblRightClickHandler,
                     self.NotesUpdatedHandler, self.ViewToggleHandler)
    self.view_format = ViewFormat.LABEL_ONLY
    self.view.SetViewFormat(self.view_format)
    self.villain = None
    self.build = None
    self.error_text = None
    self.game_time = 0.0
    self.view.AddTask(self.PollAndUpdate, 1000)

  # client api:
  # https://us.battle.net/forums/en/sc2/topic/20748195420
  def PollAndUpdate(self):
    self.error_text = None
    try:
      response = requests.get("http://localhost:6119/game")
      game_info = json.loads(response.text)
      self.game_time = game_info['displayTime']
      for player in game_info['players']:
        name = player['name']
        if self.villain is not None and name == self.villain.name:
          break
        elif name != self.cfg.hero:
          self.villain = Villain(name, self.cfg.data_dir)
          self.build = Build(player['race'], self.cfg.data_dir)
          self.view.SetNotesText(self.villain.GetNotes())
          break
      else:
        self.error_text = 'No villain found.'
    except Exception as e:
      self.error_text = "Can't connect to API."
      print (e)
    self.UpdateView(self.view_format)

  def UpdateView(self, view_format):
    # Try to change view format.
    if self.error_text is not None:
      if view_format == ViewFormat.TAB:
        self.view_format = view_format
      else:
        self.view_format = ViewFormat.LABEL_ONLY
    elif view_format == ViewFormat.TAB or view_format == ViewFormat.LABEL_ONLY:
      self.view_format = view_format
    elif view_format == ViewFormat.NOTES_VIEW:
      if self.villain is not None:
        self.view_format = view_format
    elif view_format == ViewFormat.BUILD_VIEW:
      if self.build is not None:
        self.view_format = view_format

    # Set label text
    if self.view_format == ViewFormat.TAB:
      self.view.SetLabelText('')
    elif self.error_text is not None:
      self.view.SetLabelText(self.error_text)
    elif self.view_format == ViewFormat.BUILD_VIEW:
      self.view.SetLabelText('{}: {}'.format(self.build.race, self.build.name))
    else:
      self.view.SetLabelText(self.villain.name)

    # Other stuff
    if self.view_format == ViewFormat.BUILD_VIEW:
      self.view.SetBuildText(
        past=self.build.GetBuildText(before=self.game_time),
        future=self.build.GetBuildText(earliest=self.game_time))
    self.view.SetViewFormat(self.view_format)


  def Run(self):
    self.view.Run()

  # Make us smaller.
  def LblLeftClickHandler(self, e):
    if self.view_format == ViewFormat.TAB:
      pass
    elif self.view_format == ViewFormat.LABEL_ONLY:
      self.UpdateView(ViewFormat.TAB)
    else:
      self.UpdateView(ViewFormat.LABEL_ONLY)

  # Make us bigger.
  def LblRightClickHandler(self, e):
    if self.view_format == ViewFormat.TAB:
      self.UpdateView(ViewFormat.LABEL_ONLY)
    elif self.view_format == ViewFormat.LABEL_ONLY:
      self.UpdateView(ViewFormat.NOTES_VIEW)

  def NotesUpdatedHandler(self, e):
    self.villain.SaveNotes(self.view.GetVillainNotes())

  def ViewToggleHandler(self):
    if self.view_format == ViewFormat.NOTES_VIEW:
      self.UpdateView(ViewFormat.BUILD_VIEW)
    elif self.view_format == ViewFormat.BUILD_VIEW:
      self.UpdateView(ViewFormat.NOTES_VIEW)
