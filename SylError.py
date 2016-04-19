from Constants import Constants
from Penalty import Penalty

class SylError:
  def __init__(self):
    self.ref = {}
    self.hyp = {}
    self.alignedHyp = {}
    self.struct = ()

    self.errors   = {}
    self.errors[Constants.OTHER] = []

    self.pen = 0

  def disp(self):
    labels = [Constants.ONSET, \
            Constants.NUCLEUS, \
            Constants.CODA, \
            Constants.TONE]

    s = "REF:\t\t\t\t\t{ "
    for l in labels:
      if l in self.ref:
        s = s + l + ": " + self.ref[l] + ", "
    s = s + "}\n"

    s = s +  "HYP:\t\t\t\t\t{ " + Constants.OTHER + ": " + ' '.join(self.hyp[Constants.OTHER]) + \
            ", "  + Constants.TONE + ": " + self.hyp[Constants.TONE] + " }\n"

    s = s +  "ALIGNED HYP:\t{ "
    for l in labels:
      if l in self.alignedHyp:
        s = s + l + ": " + self.alignedHyp[l] + ", "
    s = s + "}\n"
    s = s +  "STRUCT:\t\t\t\t" + str(self.struct) + "\n"

    s = s +  "ERRORS:\t\t\t\t{ "
    for l in labels:
      if l in self.errors:
        s = s + l + ": " + self.errors[l] + ", "
    s = s + "}\n"

    s = s +  "PENALTY:\t\t\t" + str(self.pen) + "\n\n"
    return s
 
  def evalScliteOutput(self, hParts, scliteOutput):
    ref = scliteOutput[Constants.REF][6:] + Constants.DELIM
    hyp = scliteOutput[Constants.HYP][6:] + Constants.DELIM
    err = scliteOutput[Constants.EVAL][6:] + Constants.DELIM

    rTok = ''
    hTok = ''
    errTok = ''
    rTokCount = 0
    hTokCount = 0

    for i in range(len(ref)):
      rTok = rTok.strip()
      hTok = hTok.strip()
      errTok = errTok.strip()

      if ref[i] == Constants.DELIM:
        if len(rTok) > 0 and Constants.DELETED not in rTok:
          if errTok == '':
            errTok = Constants.CORRECT

          label = self.struct[rTokCount]
          self.errors[label] = errTok
          self.alignedHyp[label] = hTok

          rTokCount = rTokCount + 1
        else:
          self.errors[Constants.OTHER].append(errTok)

        if Constants.DELETED not in hTok:
          hTokCount = hTokCount + 1

        rTok = ''
        hTok = ''
        errTok = ''
      else:
        rTok = rTok + ref[i]
        if i < len(hyp):
          hTok = hTok + hyp[i]
        if i < len(err):
          errTok = errTok + err[i]
    # print self.ref
    # print self.alignedHyp
    # print self.errors


  def constructPen(self, hParts, hTone, rParts, rTone, scliteOutput, langSpecs):
    self.processRefSylStruct(rParts, langSpecs)
    self.evalScliteOutput(hParts, scliteOutput)

    self.hyp[Constants.TONE] = hTone
    self.hyp[Constants.OTHER] = hParts
    self.ref[Constants.TONE] = rTone

    self.errors[Constants.TONE] = Constants.CORRECT
    if hTone != rTone:
      self.errors[Constants.TONE] = Constants.SUB
    elif hTone == '':
      self.errors[Constants.TONE] = Constants.DEL

    self.computePen()

  def computePen(self):
    self.pen = 0
    for label in [Constants.ONSET, Constants.NUCLEUS, Constants.CODA, Constants.TONE]:
      if label in self.ref:
        err = self.errors[label]
        self.pen = self.pen + Penalty.vals[label][err]
    for err in self.errors[Constants.OTHER]:
      if err:
        self.pen = self.pen + Penalty.vals[Constants.OTHER][err]


  def processRefSylStruct(self, rParts, langSpecs):
    if len(rParts) == 3:
      self.ref[Constants.ONSET] = rParts[0]
      self.ref[Constants.NUCLEUS] = rParts[1]
      self.ref[Constants.CODA] = rParts[2]
      self.struct = (Constants.ONSET, Constants.NUCLEUS, Constants.CODA) 
    elif len(rParts) == 2:
      if rParts[0] in langSpecs[Constants.NUCLEUS]:
        self.ref[Constants.NUCLEUS] = rParts[0]
        self.ref[Constants.CODA] = rParts[1]
        self.struct = (Constants.NUCLEUS, Constants.CODA)
      if rParts[0] in langSpecs[Constants.ONSET]:
        self.ref[Constants.ONSET] = rParts[0]
        self.ref[Constants.NUCLEUS] = rParts[1]
        self.struct = (Constants.ONSET, Constants.NUCLEUS)
    elif len(rParts) == 1:
      self.ref[Constants.NUCLEUS] = rParts[0]
      self.struct = (Constants.NUCLEUS)
    else:
      print("Reference syllable with an invalid length!")
      exit

#  newSylErr = SylError()
#  sample = {}
#  dummy = {}
#  sample['REF']  = 'REF:  b_< U K'
#  sample['HYP']  = 'HYP:  b_< * O'
#  sample['Eval'] = 'Eval:     D S'
#  rParts = ['b_<','u', 'k']
#  rTone = '_3'
#  hParts = ['b_<', 'o']
#  hTone  = '_2'
#  # newSylErr.processRefSylStruct(rParts, dummy)
#  # newSylErr.evalScliteOutput(hParts, sample)
#  newSylErr.constructPen(hParts, hTone, rParts, rTone, sample, dummy)
#  
#  sample['REF']  = 'REF:  b_< U K'
#  sample['HYP']  = 'HYP:  d   U O'
#  sample['Eval'] = 'Eval: S     S'
#  hParts = ['d', 'u', 'o']
#  hTone  = ''
#  # newSylErr.processRefSylStruct(rParts, dummy)
#  # newSylErr.evalScliteOutput(hParts, sample)
#  newSylErr.constructPen(hParts, hTone, rParts, rTone, sample, dummy)
#  
#  sample['REF']  = 'REF:  b_< U K'
#  sample['HYP']  = 'HYP:  d   U O'
#  sample['Eval'] = 'Eval: S      '
#  # newSylErr.processRefSylStruct(rParts, dummy)
#  # newSylErr.evalScliteOutput(hParts, sample)
#  newSylErr.constructPen(hParts, hTone, rParts, rTone, sample, dummy)
#  
#  sample['REF']  = 'REF:  s * * @: n'
#  sample['HYP']  = 'HYP:  * R U @: N'
#  sample['Eval'] = 'Eval: D I I C  S'
#  rParts = ['s', '@:', 'n']
#  hParts = ['r', 'u', '@:', 'n']
#  # newSylErr.processRefSylStruct(rParts, dummy)
#  # newSylErr.evalScliteOutput(hParts, sample)
#  newSylErr.constructPen(hParts, hTone, rParts, rTone, sample, dummy)

