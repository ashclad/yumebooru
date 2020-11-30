import logging
import re as rgx
from yaml import load as unyammify
from yaml import dump as yammify
from json import loads as antijason
from json import dumps as jason

# move dictlookup to other py file
def dictlookup(k="",d={},spittype=None,nest=False,num=0,update=[],handler=None):
  # see if there are ways to rewrite this
  if nest and isinstance(k,str):
    num += 1
    if num >= 1:
      if k not in d:
        update.append(k)
        for v in d.values():
          if isinstance(v,dict):
            return dictlookup(k,v,nest=True,update=update)
      elif k in d:
        update.append(k)
        update.reverse()
        return update
  else:
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

def dictalter(sought=[],stack={},handler=None,newkey=None,num=0):
  # finish this recursive function to get to correct entry; itertools
  hand = handler
  if num >= 0:
    num += 1
    if newkey == None:
      new = dictlookup(sought,stack,"key")
    else:
      new = dictlookup(sought,stack[newkey],"key")
  return dictalter(sought,stack,hand,new,num)

class Config:
  def __init__(self,configdict,**kwargs):
    self.initdict = configdict
    if isinstance(configdict, dict):
      for k,v in configdict.items():
        setattr(self,k,v)
    else:
      raise TypeError

  def get(self,spittype="dict",entry=[]):
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
        result = dictlookup(entry,self.__dict__,"value")
      elif isinstance(entry,list):
        result = dictlookup(entry,self.__dict__,"value")
    else:
      result = self.__dict__

    if spittype == "dict" or spittype == "python" or spittype == "native":
      return result
    elif spittype == "yaml" or spittype == "yml":
      return yammify(result)
    elif spittype == "json":
      return jason(result)

  def set(self,insertion,into=[],spittype="dict"):
    def changeentry(stack,target):
      stack[target] = insertion

    if len(into) > 0:
      if isinstance(into,str):
        if rgx.search("->", into):
          into = into.split("->")
        elif rgx.search(".", into):
          into = into.split(".")
        elif rgx.search("][", into):
          del into[0]
          del into[-1]
          into = into.split("][")

        if isinstance(insertion,dict):
          result = dictlookup(into,self.__dict__,"value")
      elif isinstance(into,list):
        if isinstance(insertion,dict):
          result = dictlookup(nt,self.__dict__,"value")

    if spittype == "dict" or spittype == "python" or spittype == "native":
      return result
    elif spittype == "yaml" or spittype == "yml":
      return yammify(result)
    elif spittype == "json":
      return jason(result)

  def add(self,insertion,into=""):
    pass

  def __add__(self,other):
    return Config(other.__dict__.update(other.__dict__))

