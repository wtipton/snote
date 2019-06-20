import os

class Villain:
  def __init__(self, name, data_dir):
    self.name = name
    self.path = os.path.join(data_dir, 'notes', name)

  def GetNotes(self):
    try:
      with open(self.path) as f:
        return f.read()
    except:
      print(self.name, " is new i guess!")
      return ''

  def SaveNotes(self, notes):
    with open(self.path, 'w') as f:
      f.write(notes)
