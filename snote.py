# Note theres a hack in tk that make overrideredirect windows not get focus:
# http://core.tcl.tk/tk/artifact/7892c68f49012d2d71222ae0e312a1e7dc69a801?txt=1&ln=51-64
# can apt-get source libtk8.6, delete it, and dpkg-buildpackage -rfakeroot -uc -b
#
# So the redirectoverride thing is basically a way to get top stacking order.
# Can also get that from a window manager. In openbox, had to hack stacking.cc to
# put ABOVE windows above FULLSCREEN windows. Could also probably add new
# functionality to calc_layer in client.cc. But still have focus problems.
from tkinter import *
import json
import requests
 
#root = Tk()
#window = Toplevel()
window = Tk()
#window.title("Welcome to LikeGeeks app")

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

lbl = Label(window, text="Loading...")
lbl.grid(column=0, row=0, sticky=E+W)

toggle=False
def clicked(e):
    global height, toggle
    toggle = not toggle
    resize_window(toggle)
lbl.bind("<Button-1>", clicked)

S = Scrollbar(window)
T = Text(window, height=4, width=50)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
T.grid(column=0,row=1, sticky="ewns")
S.grid(column=1,row=1, sticky="ns")

#btn = Button(window, text="Notes", command=clicked)
#btn.grid(column=0, row=0)

def notes_path(username):
  notes_dir='/home/wtipton/projects/snote/data/notes/'
  return notes_dir + username

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
#open_user(villain)

def update_notes(e):
  notes = T.get(1.0, END)
  with open(notes_path(villain), 'w') as f:
    f.write(notes)
T.bind("<Key>", update_notes)

# client api:
# https://us.battle.net/forums/en/sc2/topic/20748195420
def poll_and_update():
  hero = 'pzlin'
  #window.focus_force()
  #window.lift()
  try:
    response = requests.get("http://localhost:6119/game")
    game_info = json.loads(response.text)
    for player in game_info['players']:
      name = player['name']
      if name == villain:
        break
      elif name != hero:
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
