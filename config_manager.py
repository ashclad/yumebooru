import logging
import re as rgx
from yaml import load as unyammify
from yaml import dump as yammify
from json import loads as antijason
from json import dumps as jason

def get_entry(target_dict,listofkeys):
  if len(listofkeys) > 0:
    for k in listofkeys:
      for i in range(len(listofkeys)):
        get_entry(target_dict[k],listofkeys[(i+1):len(listofkeys)])
  else:
    return target_dict

class Config:
  def __init__(self,configdict):
    self.dictionary = configdict
    if isinstance(configdict, dict):
      for k,v in configdict.items():
        setattr(self,k,v)
    else:
      raise TypeError

  def get(self,spittype="dict",entry=None):
    if entry != None:
      if isinstance(entry,str):
        if rgx.search("->", entry):
          entry = entry.split("->")
        elif rgx.search(".", entry):
          entry = entry.split(".")
        elif rgx.search("][", entry):
          del entry[0]
          del entry[-1]
          entry = entry.split("][")
        result = get_entry(__dict__,entry)
      elif isinstance(entry,list):
        result = get_entry(__dict__,entry)
    else:
      result = self.dictionary

    if spittype == "dict" or spittype == "python" or spittype == "native":
      return result
    elif spittype == "yaml" or spittype == "yml":
      return yammify(result)
    elif spittype == "json":
      return jason(result)

  def set(self,insert,entry=None):
    pass

