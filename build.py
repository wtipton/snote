import os
import yaml

class Build:
  def __init__(self, name, data_dir):
    self.name = name
    path = os.path.join(data_dir, 'builds', name)
    with open(path, 'r') as ymlfile:
      self.build = yaml.safe_load(ymlfile)

  def GetBuildText(self):
    return str(self.build)