import logging
from yaml import load as unyammify
from yaml import dump as yammify
# import passlib.context import CryptContext as cryptset # prefer bcrypt_sha256
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

conffile = './config.yaml'
with open(conffile, 'r') as bindata:
  config = bindata.read()
  config = unyammify(config)

dbinfo = config['database']
dbscheme = dbinfo['scheme'].split(':')

if rgx,search("\+", dbscheme[0]):
  dbtype = dbscheme[0].split('+')[0]

app = Flask(__name__)

if dbscheme[0] == "sqlite" or dbtype == "sqlite":
  if len(dbscheme[1]) < 3:
    dburi = dbinfo['scheme'] + "/" + dbinfo['namepath'] + "." + dbinfo['ext']
  elif len(dbscheme[1]) > 4:
    for strikenum in range(len(dbscheme[1])):
      if strikenum > 4:
        del dbscheme[1][strikenum]
    dburi = dbscheme[0] + ":" + dbscheme[1] + "/" + dbinfo['namepath'] + "." + dbinfo['ext']
  app.config['SQLALCHEMY_DATABASE_URI'] = dburi
else:
  if dbinfo['password'] != False:
    # get tuple of password string from user input in other py file that is supposed to produce config.yaml
    # use that in place of dbinfo['password']
    if dbinfo['port'] != False:
      dburi = dbinfo['scheme'] + dbinfo['user'] + ":" + dbinfo['password'] + "@" + dbinfo['host'] + ":" + dbinfo['port'] + "/" + dbinfo['namepath']
    else:
      dburi = dbinfo['scheme'] + dbinfo['user'] + ":" + dbinfo['password'] + "@" + dbinfo['host'] + "/" + dbinfo['namepath']
  else:
    PASSWORD = (str(input("Please enter the database password: ")),)
    if dbinfo['port'] != False:
      dburi = dbinfo['scheme'] + dbinfo['user'] + ":" + PASSWORD[0] + "@" + dbinfo['host'] + ":" + dbinfo['port'] + "/" + dbinfo['namepath']
    else:
      dburi = dbinfo['scheme'] + dbinfo['user'] + ":" + PASSWORD[0] + "@" + dbinfo['host'] + "/" + dbinfo['namepath']
  app.config['SQLALCHEMY_DATABASE_URI'] = dburi

sb = SQLAlchemy(app)

@app.route('/')
def index():
  if config['engine']['construction'] or config['site']['construction']:
    return render_template("standby.html")
  else:
    return render_template("index.html")

if __name__ == "__main__":
  app.run(debug=True)
