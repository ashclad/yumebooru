import re as rgx
from yaml import load as unyammify
from yaml import dump as yammify
from json import loads as antijason
from json import dumps as jason

# move dictseek to other py file
def dictseek(k="",d={},spittype="",nest=False,update=[]):
  # see if there are ways to rewrite this
  """
  Returns a list of keys nested into, or an item/key/value
  or several of them found at any level of dictionary.
  """
  dictseek.execnum += 1
  if nest:
    if isinstance(k,str):
      if k not in d:
        update.append(k)
        for v in d.values():
          if isinstance(v,dict):
            return dictseek(k,v,nest=True,update=update)
      elif k in d:
        update.append(k)
        update.reverse()
      return update
    elif isinstance(k,list):
      arr = []
      for i in k:
        if i not in d:
          arr.append(i)
          update.append(arr)
          for v in d.values():
            if isinstance(v,dict):
              return dictseek(k,v,nest=True,update=update)
        elif i in d:
          arr.append(i)
          update.append(arr)
          update.reverse()
      return update
  else:
    if isinstance(k,str):
      if k in d:
        if isinstance(spittype,str):
          if spittype == "key":
            return k
          elif spittype == "value":
            return d[k]
          elif spittype == "item":
            for entry,definition in d.items():
              if entry == k:
                return {entry: definition}
          else:
            return None
    if isinstance(k,list):
      arr = []
      for i in k:
        if i in d:
          if isinstance(spittype,str):
            if spittype == "key":
              arr.append(i)
            elif spittype == "value":
              arr.append(d[i])
            elif spittype == "item":
              for entry,definition in d.items():
                if entry == i:
                  arr.append({entry: definition})
            else:
              return None
      return arr
    if isinstance(k,dict):
      arr = []
      for ent,exp in k.items():
        if ent in d and d[ent] == exp:
          if isinstance(spittype,str):
            if spittype == "key":
              arr.append(ent)
            elif spittype == "value":
              arr.append(exp)
            elif spittype == "item":
              arr.append({ent: exp})
            else:
              return None
      return arr
    for v in d.values():
      if isinstance(v, dict):
        return dictseek(k, v, spittype)
  return None
setattr(dictseek, 'execnum', 0)

def dicttarget(needle="",stack={},newval=""):
  # see if there are ways to rewrite this
  """
  Finds entry in dictionary and then uses a
  handler to do something with its value.
  """
  dicttarget.execnum += 1
  if isinstance(needle,str):
    for s in stack.keys():
      if s == needle:
        stack[needle] = newval
        return stack[needle]
  elif isinstance(needle,list):
    for n in needle:
      for s in stack.keys():
        if s == n:
          stack[n] = newval
          return stack[n]
  elif isinstance(needle,dict):
    for n,o in needle.items():
      for s,e in stack.items():
        if s == n and e != o:
          stack[n] = o
          return stack[n]

  for p in stack.keys():
    return dicttarget(newk,stack[p],newval)
  return None
setattr(dicttarget, 'execnum', 0)

class Config:
  """
  A class for creating and
  managing configuration
  objects.
  """
  def __init__(**kwargs):
    """
    Creates attributes of object
    based on keyword arguments.
    """
    if "config" in kwargs:
      for k,v in kwargs.items():
        if k != "config":
          del kwargs[k]
        else:
          if isinstance(kwargs['config'],dict):
            for f,s in kwargs['config'].items():
              setattr(self,f,s)
    else:
      for k,v in kwargs.items():
        setattr(self,k,v)

  def get(self,spittype="dict",entry=[]):
    """
    Acquires and spits out object attribute
    if queried object attribute exists at any
    dictionary nesting level of object.
    """
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
        result = dictseek(entry,self.__dict__,"value")
      elif isinstance(entry,list):
        result = dictseek(entry,self.__dict__,"value")
    else:
      result = self.__dict__

    if spittype == "dict" or spittype == "python" or spittype == "native":
      return result
    elif spittype == "yaml" or spittype == "yml":
      return yammify(result)
    elif spittype == "json":
      return jason(result)

  def set(self,insertion,into="",spittype="dict"):
    """
    Looks through various dictionary nesting levels
    of object dictionary for given key and changes
    its value for key at that level.
    """
    if isinstance(into,str) and len(into) > 0:
      if isinstance(insertion,str):
        result = dicttarget(into,self.__dict__,insertion)
      elif isinstance(insertion,list):
        # to write
        pass
      elif isinstance(insertion,dict):
        # to write
        pass

    if isinstance(insertion,dict):
        for i,n in insertion.items():
          result = dicttarget(i,self.__dict__,n)

    if spittype == "dict" or spittype == "python" or spittype == "native":
      return result
    elif spittype == "yaml" or spittype == "yml":
      return yammify(result)
    elif spittype == "json":
      return jason(result)

  def new(self,insertion,into=""):
    """
    Traverses dictionary nesting level
    of object to find given spot to add a new
    dictionary entry.
    """
    # to write
    pass

  def __add__(self,other):
    """
    Allows one to use addition operator to
    create new object by adding objects of
    this class together. E.g.:
      <object> = <object> + <object>
    """
    newdict = self.__dict__[:]
    newdict.update(other.__dict__)
    return Config(config=newdict)

