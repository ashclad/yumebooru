import re as rgx

def boolinput(string):
  while True:
      answer = str(input(string))
      if rgx.match("[Yy]es|[Tt]rue", answer) or rgx.fullmatch("[Yy]|[Tt]", answer):
        answer = True
        break
      elif rgx.match("[N]o |[Ff]alse", answer) or rgx.fullmatch("[Nn]|[Ff]", answer):
        answer = False
        break
      else:
        print("Unacceptable input. Please type 'yes' or 'no'.")
  return answer

def titleinput(string):
  while True:
    answer = str(input(string))
    if rgx.fullmatch("[A-Z]\w", answer):
      break
    else:
      print("Unacceptable input. Make sure to capitalize title.")
  return answer

def domaininput(string):
  while True:
    answer = str(input(string))
    if rgx.fullmatch("[Ww][Ww][Ww]\.)?([a-z.]*)\.([a-z]{3}", answer):
      break
    else:
      print("Unacceptable input. Don't forget to add TLD name.")
  return answer

def pwdinput():
  while True:
    answer = str(input(string))
    if rgx.search("[\!\@\#\$\%\^\&\*]", answer) and rgx.search("[A-Z]", answer):
      break
    else:
      print("Unacceptable input. Password must have at least ")
