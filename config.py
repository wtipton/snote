import os
import yaml

# the config is a yaml file in '~/.config/snote.yaml'
class Config:
  def __init__(self):
    cfg_file = os.path.join(os.path.expanduser('~'), '.config','snote.yaml')
    with open(cfg_file, 'r') as ymlfile:
      self.cfg = yaml.safe_load(ymlfile)

  def __getattr__(self, attr):
    return self.cfg[attr]
