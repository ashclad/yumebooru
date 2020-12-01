from types import GeneratorType as generator

def condseq(respvar,mappings={},pspace=[],iffunc=[],elfunc=[]):
  """
  Function for creating a closure function that runs a
  generated list of basic conditionals (no 'elifs'); is
  possible to create distinct functions for distinct types
  of conditionals
  """
  possib = pspace

  if callable(iffunc):
    iffunc = [iffunc]
  if callable(elfunc):
    elfunc = [elfunc]

  possib_notiter = (not (isinstance(possib,list) or isinstance(possib,tuple) or isinstance(possib,generator)))
  if possib_notiter:
    possib = [possib]

  if isinstance(mappings,dict):
    kseq = mappings.keys()
    vseq = mappings.values()

    if len(elfunc) > 0:
      pfpairs = zip(kseq,vseq,elfunc)
    else:
      pfpairs = zip(kseq,vseq)
  else:
    if len(elfunc) > 0:
      pfpairs = zip(kseq,vseq,elfunc)
    else:
      pfpairs = zip(kseq,vseq)

  def closure():
    if len(elfunc) <= 0:
      for p,f in pfpairs:
        if respvar == p:
          f()
    else:
      for p,f,f2 in pfpairs:
        if respvar == p:
          f()
        else:
          f2()

  return closure
