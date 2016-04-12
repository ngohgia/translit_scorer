class SylError:
  ONSET = 'ONSET'
  NUCLEUS = 'NUCLEUS'
  CODA = 'CODA'

  CORRECT = 'C'
  SUB     = 'S'
  DEL     = 'D'
  INS     = 'I'

  def __init__(self):
    self.ref = {}
    self.hyp = {}
    self.struct = ()

    self.onset   = CORRECT
    self.nucleus = CORRECT
    self.coda    = CORRECT

  def computePen(oParts, oTone, rParts, rTone, ref, score):
    processRefSylStruct(rParts)

    count = 0
    for c in ref:
      if c == ' ':
        role = self.struct[count]
        self.hyp[role] = oParts[count]
    print self.hyp
    exit()

  def processRefSylStruct(ref_parts):
    if len(ref_parts) == 3:
      self.ref[ONSET] = ref_parts[0]
      self.ref[NUCLEUS] = ref_parts[1]
      self.ref[CODA] = ref_parts[2]
      self.struct = (ONSET, NUCLEUS, CODA) 
    elif len(ref_parts) == 2:
      if ref_parts[0] in langSpecs[NUCLEUS]:
        self.ref[NUCLEUS] = ref_parts[0]
        self.ref[CODA] = ref_parts[1]
        self.struct = (NUCLEUS, CODA)
      if ref_parts[0] in langSpecs[ONSET]:
        self.ref[ONSET] = ref_parts[0]
        self.ref[NUCLEUS] = ref_parts[1]
        self.struct = (ONSET, NUCLEUS)
    elif len(ref_parts) == 1:
      self.ref[NUCLEUS] = ref_parts[0]
      self.struct = (NUCLEUS)
    else:
      print("Reference syllable with length 0!")
      exit
