import os

class Villain:
  def __init__(self, name, data_dir):
    self.name = name
    self.path = os.path.join(data_dir, 'notes', name)
    try:
      with open(self.path) as f:
        self.notes = f.read()
    except:
      print(self.name, " is new i guess!")
      self.notes = ''

  def GetNotes(self):
    print (self.notes)
    return self.notes

  def SaveNotes(self, notes):
    self.notes = notes
    with open(self.path, 'w') as f:
      f.write(self.notes)
