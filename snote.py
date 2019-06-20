#!/usr/bin/python3

import json
import os
import requests
import tkinter as tk

import config

cfg = config.Config()

#root = tk.Tk()
#window = tk.Toplevel()
window = tk.Tk()
window.title("snote")

#window.overrideredirect(True)
#window.wm_attributes('-type','splash')
#window.lift()
window.wm_attributes("-topmost", True)
#window.wm_attributes("-disabled", True)
#window.wm_attributes("-transparentcolor", "white")

# https://stackoverflow.com/questions/28419763/expand-text-widget-to-fill-the-entire-parent-frame-in-tkinter
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)

def resize_window(show_text_area):
  width=300
  if show_text_area:
    height = 300
  else:
    height = 18
  window.geometry(str(width)+"x"+str(height)+"+5+700")
resize_window(False)

lbl = tk.Label(window, text="Loading...")
lbl.grid(column=0, row=0, sticky=tk.E+tk.W)

toggle=False
def clicked(e):
    global height, toggle
    toggle = not toggle
    resize_window(toggle)
lbl.bind("<Button-1>", clicked)

S = tk.Scrollbar(window)
T = tk.Text(window, height=4, width=50)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
T.grid(column=0,row=1, sticky="ewns")
S.grid(column=1,row=1, sticky="ns")

#btn = tk.Button(window, text="Notes", command=clicked)
#btn.grid(column=0, row=0)

def notes_path(username):
  return os.join.path(cfg.data_dir, 'notes', username)

villain = 'bob'
def open_user(username):
  global villain
  villain = username
  lbl.configure(text=username)
  T.delete(1.0, END)
  try:
    with open(notes_path(username)) as f:
      notes = f.read()
      T.insert(END, notes)
  except:
    print(username, " is new i guess!")
  T.configure(state=NORMAL)      

def update_notes(e):
  notes = T.get(1.0, END)
  with open(notes_path(villain), 'w') as f:
    f.write(notes)
T.bind("<Key>", update_notes)

# client api:
# https://us.battle.net/forums/en/sc2/topic/20748195420
def poll_and_update():
  #window.focus_force()
  #window.lift()
  try:
    response = requests.get("http://localhost:6119/game")
    game_info = json.loads(response.text)
    for player in game_info['players']:
      name = player['name']
      if name == villain:
        break
      elif name != cfg.hero:
        open_user(name)
        break
    else:
      print('couldnt identify villain in api output')
  except:
    print ('couldnt open game api')
  window.after(2000, poll_and_update)
poll_and_update()

#def EnsureTop():
#  window.lift()
#  window.focus()
#  window.after(1000, EnsureTop)
#  window.wm_attributes("-topmost", True)
#EnsureTop()

window.mainloop()
