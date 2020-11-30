import logging
from passlib.context import CryptContext as crypttype
from yaml import load as unyammify
from yaml import dump as yammify
from random import choice as selectfrom
import os
import re as rgx
import pyinputplus as pyip
from requests import get as urlget
from toascii import Image as ascimg
from .ssl_manager import TLSman as tls

cryptic = crypttype(schemes=["bcrypt_sha256","des_crypt"])
encrypt = cryptic.hash

print("Welcome to Yumebooru!")

"""
Sets directory this runs from as application root.
"""
APPROOT = os.path.abspath(os.curdir)

"""
If file exists, change contents. Otherwise, begin creating new file.
"""
if os.path.exists('config.yaml') and os.path.isfile('config.yaml'):
  print("Setup has already been completed at least once.")
  wantchange = pyip.inputYesNo(prompt="Would you like to make any configuration changes? ", default="yes", limit=3)
  if wantchange == 'yes':
    # create function to call here for changing config file
  else:
    print("Then there is no need for you to use this here.")
    # use toascii module to show ascii art based on local image
    exitwish = inputYesNo("Do you wish to exit?",default="yes",limit=1)
    if exitwish == "yes":
      exit()
else:
  print("Setup initiated...")
  SITENAME = pyip.inputStr(prompt="How would you like to name your imageboard? ",default="Yumebooru",limit=3,whitelistRegexes=["[A-Z]\w+"])
  hostused = pyip.inputYesNo(prompt="Are you running experimentally on local machine? ",default="yes",limit=3)
  ip6 = pyip.inputYesNo(prompt="Do you wish to use IPv6? ",default="no",limit=3)
  tlsused = pypi.inputYesNo("Will your server use TLS connections? ",default="no",limit=3)

  if hostused == "yes":
    if ip6 == "no":
      SITEHOST = selectfrom(["localhost","127.0.0.1"])
    else:
      SITEHOST = "[::1]"

    SITEPORT = pyip.inputInt("What port will your site's server be using? ",default=80,limit=3)

    if tlsused == "yes":
      URISCHEME = "https://"
      # make arguments below user-acquired or ping-acquired
      SERVID = tls(SITEHOST,cntry="US",stt="New York",cty="New York",org="Sample Services Institute")
      targetpath = os.path.join(os.path.abspath(os.curdir), "static/.well-known")
      if os.path.exists(targetpath) and os.path.isdir(targetpath):
        TLSINFO = SERVID.gencert(targetpath)
      else:
        os.makedirs(targetpath)
        SERVID.gencert(targetpath)
      #TLSINFO = SERVID.pubcert() # this code is for production
      #TLSINFO['path'] = "static/.well-known" # this code is for production
      TLSINFO = None
      # reformat TLSINFO['dir']? # this will be for production
    else:
      URISCHEME = "http://"
    if SITEPORT = 80:
      BASEURL = URISCHEME + SITEHOST
    else:
      BASEURL = URISCHEME + SITEHOST + ":" + SITEPORT
  else:
    if ip6 == "no":
      public4 = urlget('https://api.ipify.org').text
      SITEDOMAIN = pyip.inputStr("What is the domain name or public IP for your address? ",default=public4,limit=3,whitelistRegexes=["([Ww][Ww][Ww]\.)?([a-z.]*)\.([a-z]){3}","([0-9]*\.){3}[0-9]*"])
    else:
      public6 = urlget('https://api64.ipify.org').text
      SITEDOMAIN = pyip.inputStr("What is the domain name or public IP for your address? ",default=public6,limit=3,whitelistRegexes=["([Ww][Ww][Ww]\.)?([a-z.]*)\.([a-z]){3}","([a-z0-9]*:){2,7}[a-z0-9]*"])

    domainlist = SITEDOMAIN.split(".")

    if rgx.fullmatch("\.([a-z]){3}",domainlist[len(domainlist)-1]):
      SITETLD = domainlist[len(domainlist)-1]
      TRUESITEDOMAIN = domainlist[len(domainlist)-2]
      if rgx.fullmatch("[Ww][Ww][Ww]", domainlist[0]):
        del domainlist[0]
        SITEDOMAIN = ".".join(domainlist)
    else:
      SITETLD = None
      TRUESITEDOMAIN = None

    SITEPORT = pyip.inputInt("What port will your site's server be using? ",default=80,limit=3)

    if tlsused == "yes":
      URISCHEME = "https://"
       # make arguments below user-acquired or ping-acquired
      SERVID = tls(SITEHOST,cntry="US",stt="New York",cty="New York",org="Sample Services Institute")
      targetpath = os.path.join(os.path.abspath(os.curdir), "static/.well-known")
      if os.path.exists(targetpath) and os.path.isdir(targetpath):
        TLSINFO = SERVID.gencert(targetpath)
      else:
        os.makedirs(targetpath)
        SERVID.gencert(targetpath)
      #TLSINFO = SERVID.pubcert() # this code is for production
      #TLSINFO['path'] = "static/.well-known" # this code is for production
      TLSINFO = None
      # reformat TLSINFO['dir']? # this will be for production
    else:
      URISCHEME = "http://"
    if SITEPORT = 80:
      BASEURL = URISCHEME + SITEHOST
    else:
      BASEURL = URISCHEME + SITEHOST + ":" + SITEPORT

  SITEDESC = inputStr("Describe your website: \n",default="",limit=3) # make pseudo-rich text
  ismanual = inputYesNo("Did you already manually create a database for Yumebooru? ",default="yes",limit=3)
  dbname_q = "What is the name of the database to be accessed? "
  dbhost_q = "What is the hostname or domain name address of the database server? "
  dbport_q = "What is the port of the database server? "
  dbusr_q = "Enter the database username: "
  dbpwd_q = "Enter the database password: "

  """
  If user confirms having already created a DBMS user and database,
  have them manually input this information. Otherwise, have
  Python create the DBMS user and database.
  """
  if ismanual == "yes":
    whatdbms = inputStr("What is the database management system you'll be using? ")
    DBEXT = False

    if rgx.fullmatch("[Ss][Qq][Ll][Ii][Tt][Ee]", whatdbms):
      DBSCHEME = "sqlite://"
      DBNAME = inputStr(dbname_q)
      isext = inputBool("Does the filename have an additional file extension? ")

      if isext:
        while True:
          DBEXT = inputStr("What is the file extension? ")
          if rgx.fullmatch("[a-z0-9]{3}", DBEXT):
            break
          else:
            print("Unacceptable input.")
    elif rgx.search("([Ss][Qq][Ll])", whatdbms):
      if rgx.fullmatch("[Mm][Yy][Ss][Qq][Ll]", whatdbms):
        DBSCHEME = "mysql://"
      elif rgx.fullmatch("[Mm][Ss][Ss][Qq][Ll]", whatdbms):
        DBSCHEME = "mssql://"
      elif rgx.fullmatch("[Pp][Oo][Ss][Tt][Gg][Rr][Ee][Ss][Qq][Ll]", whatdbms):
        DBSCHEME = "postgresql://"
      DBHOST = inputStr(dbhost_q)
      DBPORT = inputStr(dbport_q)
      DBNAME = inputStr(dbname_q)
      DBUSR = inputStr(dbusr_q)
      DBPWD = inputStr(dbpwd_q)
    elif rgx.fullmatch("[Oo][Rr][Aa][Cc][Ll][Ee]", whatdbms):
      DBSCHEME = "oracle://"
      DBHOST = inputStr(dbhost_q)
      DBPORT = inputStr(dbport_q)
      DBNAME = inputStr(dbname_q)
      DBUSR = inputStr(dbusr_q)
      DBPWD = inputStr(dbpwd_q)
  else:
    # write code for automatic DBMS user and database creation
    pass

  print("Setting up configuration...")

  """
  Creates dictionary with user-acquired values. Outputs to yaml
  file, hence DBMS user password is encrypted, decrypted after
  yaml output. Same dictionary is then turned into an object.
  """
  configdict = {
    "setup": True,
    "engine": {
      "version": [0.0], # create version py file for filling out sequence
      "name": "Yumebooru",
      "type": "Application",
      "context": "https://www.w3.org/ns/activitystreams",
      "construction": False,
      "root": APPROOT
    },
    "site": {
      "name": SITENAME,
      "base_url": BASEURL,
      "id": BASEURL,
      "summary": SITEDESC,
      "construction": False
    },
    "database": {
      "scheme": DBSCHEME,
      "namepath": DBNAME,
      "ext": DBEXT,
      "host": DBHOST,
      "port": DBPORT,
      "user": DBUSR,
      "password": encrypt(DBPWD)
    }
  }
  if tlsused == "yes":
    configdict["tls"] = {
      "setup": TLSINFO['status'],
      "path": TLSINFO['path'],
      "certificate": TLSINFO['certificate'],
      "key": TLSINFO['key']
    }

  # immediately below is for production
  #conffile = 'config.yaml'
  #with open(conffile, 'w') as bindata:
  #  config = yammify(configdict, bindata, sort_keys=True)

# change permissions of 'config' yaml file
exit()
