import re as rgx
from OpenSSL import crypto as cryptgen
# from OpenSSL import SSL #look into this
from socket import gethostname
# from time import gmtime # look into this
import os.path as trace

class TLSman:
  def __init__(self,hostname=gethostname(),**kwargs):
    self.DIR = None
    self.CERT = None
    self.KEY = None
    self.CERTFILE = hostname + ".crt"
    self.KEYFILE = hostname + ".key"
    self.domain = hostname
    for k,v in kwargs.items():
      if rgx.fullmatch("([Cc]([Oo][Uu])?[Nn][Tt][Rr][Yy])|([Tt][Ee]?[Rr]{1,2}[Ii]?[Tt][Oo]?[Rr][Yy])",k):
        self.country = v
      elif rgx.fullmatch("([Ss][Tt][Aa]?[Tt][Ee]?)|([Pp][Rr][Oo][Vv]([Ii][Nn][Cc][Ee])?)",k):
        self.state = v
      elif rgx.fullmatch("([Cc][Ii]?[Tt][Yy])|([Cc]([Oo][Uu])?[Nn][Tt][Yy])",k):
        self.city = v
      elif rgx.fullmatch("([Cc][Oo]?[Mm][Pp](([Aa][Nn])|[Nn])?[Yy])|([Bb]([Uu]|[Ii])?[SsZz]{1,2}([Ii]?[Nn]([Ee][Ss])?[Ss])?)",k):
        self.company = v
      elif rgx.fullmatch("([Oo][Rr][Gg]([Aa]?[Nn]([Ii][Zz][Aa][Tt][Ii][Oo][Nn])?)?)|([Ss][Cc]([Hh]([Oo][Oo]?)?)?[Ll])|([Ii][Nn][Ss][Tt](([Ii][Tt][Uu])?[Tt][Ee]?)?)",k):
        self.organization = v

  def gencert(self,certdir,autopub=False):
    """
    If no certificate, defines internal attributes with certificate
    and key pair data. And returns an object with a certificate and key
    pair.
    """
    if not trace.exists(trace.join(certdir, self.CERTFILE)) or not trace.exists(trace.join(certdir, self.KEYFILE)):
      """
      Creates key pair
      """
      keygen = cryptgen.PKey()
      keygen.generate_key(cyptgen.TYPE_RSA,4096)

      """
      Creates certificate
      """
      certgen = cryptgen.X509()

      # create conditional checks to see if attributes exist
      certgen.get_subject().C = self.country
      certgen.get_subject().ST = self.state
      certgen.get_subject().L = self.city
      certgen.get_subject().O = self.company
      certgen.get_subject().OU = self.organization
      certgen.get_subject().CN = self.domain
      certgen.set_serial_number(1000) # look into this
      certgen.gmtime_adj_notBefore(0) # look into this
      certgen.gmtime_adj_notAfter(10*365*24*60*60) # look into this
      certgen.set_issuer(certgen.get_subject())
      certgen.set_pubkey(keygen)
      certgen.sign(keygen, 'sha1')

    self.DIR = certdir
    self.CERT = certgen
    self.KEY = keygen

    if autopub:
      self.pubcert()

    return {"dir": certdir, "certificate_data": certgen, "certificate_file": self.CERTFILE, "key_data": keygen, "key_file": self.KEYFILE}

  def pubcert(self):
    """
    Writes certificate and key attribute data to PEM files, and
    returns what was written inside a dictionary.
    """
    tlsdict = {
      "status": False,
      "dir": self.DIR,
      "certificate": "",
      "key": ""
    }
    with open(trace.join(self.DIR,self.CERTFILE), 'w+') as cf:
      cf.write(cryptgen.dump_certificate(cryptgen.FILETYPE_PEM,self.CERT))
      tlsdict['certificate'] = self.CERTFILE
    with open(trace.join(self.DIR,self.KEYFILE), 'w+') as kf:
      kf.write(cryptgen.dump_certificate(cryptgen.FILETYPE_PEM,self.KEY))
      tlsdict['key'] = self.KEYFILE

    tlsdict['status'] = True

    return tlsdict

  def verifycert(self):
    # write a way to verify certificates
    pass
