import os
import yaml

class Build:
  def __init__(self, race, data_dir):
    path = os.path.join(data_dir, 'builds', race)
    with open(path, 'r') as ymlfile:
      self.build = yaml.safe_load(ymlfile)
    self.race = race
    self.name = self.build['name']

  def __TimeStrToFloat(self, s):
    result = 0.0
    for component in s.split(':'):
      result *= 60
      result += float(component)
    return result

  def GetBuildText(self, earliest=0.0, before=float('inf')):
    lines = []
    for i in self.build['build']:
      time_sec = self.__TimeStrToFloat(i['time'])
      if earliest <= time_sec < before:
        lines.append('[{}] {}'.format(i['time'], i['item']))
    return '\n'.join(lines)
