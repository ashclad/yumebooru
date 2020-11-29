import logging
import re as rgx
from yaml import load as unyammify
from yaml import dump as yammify
from json import loads as antijason
from json import dumps as jason

# reqrite these recursive search functions
def dictlookup(k, d, spittype="item"):
  if isinstance(k,str):
    if k in d:
      if spittype == "key":
        return k
      elif spittype == "value":
        return d[k]
      elif spittype == "item":
        for entry,definition in d.items():
          if entry == k:
            return {entry: definition}
  if isinstance(k,list):
    arr = []
    for i in k:
      if i in d:
        if spittype == "key":
          arr.append(i)
        elif spittype == "value":
          arr.append(d[i])
        elif spittype == "item":
          for entry,definition in d.items():
            if entry == i:
              arr.append({entry: definition})
    return arr
  if isinstance(k,dict):
    arr = []
    for ent,exp in k.items():
      if ent in d:
        if spittype == "key":
          arr.append(ent)
        elif spittype == "value":
          arr.append(exp)
        elif spittype == "item":
          arr.append({ent: exp})
    return arr
  for v in d.values():
    if isinstance(v, dict):
      return dictlookup(k, v, spittype)
  return None

class Config:
  def __init__(self,configdict,**kwargs):
    self.initdict = configdict
    if isinstance(configdict, dict):
      for k,v in configdict.items():
        setattr(self,k,v)
    else:
      raise TypeError

  def get(self,spittype="dict",entry=""):
    if len(entry) > 0:
      if isinstance(entry,str):
        if rgx.search("->", entry):
          entry = entry.split("->")
        elif rgx.search(".", entry):
          entry = entry.split(".")
        elif rgx.search("][", entry):
          del entry[0]
          del entry[-1]
          entry = entry.split("][")
        result = dictlookup(entry,self.__dict__)
      elif isinstance(entry,list):
        result = dictlookup(self.__dict__,entry)
    else:
      result = self.__dict__

    if spittype == "dict" or spittype == "python" or spittype == "native":
      return result
    elif spittype == "yaml" or spittype == "yml":
      return yammify(result)
    elif spittype == "json":
      return jason(result)

  def set(self,insertion={},into=""):
    if len(into) > 0:
      if isinstance(into,str):
        pass
      elif isinstance(into,list):
        pass
    else:
      if isinstance(insertion,dict):
        self.__dict__.update(insertion)

  def add(self,insertion,into=""):
    pass

  def __add__(self,other):
    Config(self.__dict__ + other.__dict__)

