import logging
from passlib.context import CryptContext as crypttype
from yaml import load as unyammify
from yaml import dump as yammify
from random import choice as selectfrom
import os
import re as rgx
from .custominputs import boolinput, titleinput, domaininput, pwdinput
from .config_manager import Config

cryptic = crypttype(schemes=["bcrypt_sha256","des_crypt"])
encrypt = cryptic.hash

print("Welcome to Yumebooru!")

if os.path.isfile('config.yaml'):
  print("Setup has already been completed at least once.")
  wantchange = boolinput("Would you like to make any configuration changes? ")
  # create function to call here for changing config file
else:
  print("Setup initiated...")
  SITENAME = titleinput("How would you like to name your imageboard? ")
  hostused = boolinput("Are you running experimentally on local machine? ")

  if hostused:
    SITEHOST = selectfrom(["localhost","127.0.0.1"])
    SITEPORT = int(input("What port will your site's server be using? "))
    sslused = boolinput("Will your server use SSL connections? ")

    if sslused:
      URISCHEME = "https://"
    else:
      URISCHEME = "http://"
    if SITEPORT = 80:
      BASEURL = URISCHEME + SITEHOST
    else:
      BASEURL = URISCHEME + SITEHOST + ":" + SITEPORT
  else:
    SITEDOMAIN = domaininput("What is the domain name for your address? ")
    domainlist = SITEDOMAIN.split(".")
    SITETLD = domainlist[len(domainlist)-1]
    TRUESITEDOMAIN = domainlist[len(domainlist)-2]

    if rgx.fullmatch("[Ww][Ww][Ww]", domainlist[0]):
      del domainlist[0]
      SITEDOMAIN = ".".join(domainlist)
    sslused = boolinput("Will your server use SSL connections? ")

    if sslused:
      URISCHEME = "https://"
    else:
      URISCHEME = "http://"
    BASEURL = URISCHEME + SITEDOMAIN

  SITEDESC = str(input("Describe your website: \n")) # make pseudo-rich text
  ismanual = boolinput("Did you already manually create a database for Yumebooru? ")
  dbname_q = "What is the name of the database to be accessed? "
  dbhost_q = "What is the hostname or domain name address of the database server? "
  dbport_q = "What is the port of the database server? "
  dbusr_q = "Enter the database username: "
  dbpwd_q = "Enter the database password: "

  if ismanual:
    whatdbms = input("What is the database management system you'll be using? ")
    DBEXT = False

    if rgx.fullmatch("[Ss][Qq][Ll][Ii][Tt][Ee]", whatdbms):
      DBSCHEME = "sqlite://"
      DBNAME = str(input(dbname_q))
      isext = boolinput("Does the filename have an additional file extension? ")

      if isext:
        while True:
          DBEXT = str(input("What is the file extension? "))
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
      DBHOST = str(input(dbhost_q))
      DBPORT = str(input(dbport_q))
      DBNAME = str(input(dbname_q))
      DBUSR = str(input(dbusr_q))
      DBPWD = str(input(dbpwd_q))
    elif rgx.fullmatch("[Oo][Rr][Aa][Cc][Ll][Ee]", whatdbms):
      DBSCHEME = "oracle://"
      DBHOST = str(input(dbhost_q))
      DBPORT = str(input(dbport_q))
      DBNAME = str(input(dbname_q))
      DBUSR = str(input(dbusr_q))
      DBPWD = str(input(dbpwd_q))
  print("Setting up configuration...")
  configdict = {
    "setup": True,
    "engine": {
      "version": [0.0], # create version py file for filling out sequence
      "name": "Yumebooru",
      "type": "Application",
      "context": "https://www.w3.org/ns/activitystreams",
      "construction": False
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

  conffile = 'config.yaml'
  with open(conffile, 'w') as bindata:
    config = yammify(configdict, bindata, sort_keys=True)

  configdict["database"]["password"] = DBPWD

adminconf = Config(configdict)
