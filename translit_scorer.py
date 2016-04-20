#!/usr/bin/python

import sys
import os
from SylError import SylError
from Constants import Constants
from Penalty import Penalty

if __name__ == '__main__':
  try:
    script, sclitePath, hypPath, refPath, refLangSpecsPath = sys.argv
  except ValueError:
    print "translit_scorer.py\tsclitePath\thypPath\trefPath\trefLangSpecs"
    sys.exit(1)

SYL_DELIM = '.'
SUBSYL_DELIM = ' '
ONSET   = Constants.ONSET
NUCLEUS = Constants.NUCLEUS
CODA    = Constants.CODA
TONE    = Constants.TONE

REF     = Constants.REF
HYP     = Constants.HYP
EVAL    = Constants.EVAL

INF     = Constants.INF

#---------------------------------------------------------------------------#
def readLangSpecs(specPath):
  langSpecs = {}
  specFile = open(specPath, 'r')
  for line in specFile:
    parts = [part.strip() for part in line.split()]
    langSpecs[parts[0]] = parts[1:]
  return langSpecs

#---------------------------------------------------------------------------#
def getData(hypPath, refPath):
  hyp = []
  ref = []

  hypFile = open(hypPath, 'r');
  for line in hypFile:
    hyp.append(line.strip())
  hypFile.close()

  refFile = open(refPath, 'r');
  for line in refFile:
    ref.append(line.strip())
  refFile.close()

  if len(hyp) != len(ref):
    print "Number of hyp and reference entries do not match"
    exit(1)

  return [hyp, ref];

#--------------------------------------------------------------------------#
def ComputeScliteScore(hyp, ref, hypDir):
  reportName = 'syl_errors'
  os.system(sclitePath + " -r " + ref + \
          " -h " + hyp + \
          " -i wsj -o pra -O " + hypDir + \
          " -n " + reportName)
  return os.path.join(hypDir, reportName + '.pra')

#--------------------------------------------------------------------------#
def ComputeAllSylsErrors(hyp, ref, sclitePath, langSpecs):
  sylList = []
  
  baseDir = os.path.dirname(os.path.abspath(__file__))
  tmpDir = os.path.join(baseDir, 'tmp')

  hPartsList = []
  rPartsList = []
  hTonesList = []
  rTonesList = []

  hypSyls = [part.strip() for part in hyp.split(SYL_DELIM)]
  refSyls = [part.strip() for part in ref.split(SYL_DELIM)]
  
  idx = 1
  for hSyl in hypSyls:
    for rSyl in refSyls:
      entry = (hSyl, rSyl)
      sylList.append(entry)
  
      [hParts, hTone, rParts, rTone] = SplitTones(hSyl, rSyl)
      hPartsList.append(hParts)
      hTonesList.append(hTone)
      rPartsList.append(rParts)
      rTonesList.append(rTone)
      idx = idx + 1

  [tmpOutput, tmpRef] = WriteTmpSylFiles(hPartsList, rPartsList)
  reportPath = ComputeScliteScore(tmpOutput, tmpRef, tmpDir)
  [penalties, sylLvlPenalties] = ComputeSylLvlPenalties(reportPath, hPartsList, hTonesList, rPartsList, rTonesList, langSpecs)

  return [hypSyls, refSyls, penalties, sylLvlPenalties]


#-------------------------------------------------------------------------#
def ComputeSylLvlPenalties(reportPath, hPartsList, hTonesList, rPartsList, rTonesList, langSpecs):
  reportFile = open(reportPath, 'r')

  tmpDir = "/".join(reportPath.split("/")[:-1])
  penaltyFile = open(os.path.join(tmpDir, 'penalty_report.txt'), 'w')
  count = 0

  REF = Constants.REF
  HYP = Constants.HYP
  EVAL = Constants.EVAL

  penalties = []
  sylLvlPenalties = {}

  scliteOutput = {}
  for line in reportFile:
    line = line.strip()
    if line[:3] == REF:
      scliteOutput[REF] = line
    elif line[:3] == HYP:
      scliteOutput[HYP] = line
    elif line[:4] == EVAL:
      scliteOutput[EVAL] = line
      newSylError = SylError()

      hParts = hPartsList[count]
      hTone  = hTonesList[count]
      rParts = rPartsList[count]
      rTone  = rTonesList[count]
      newSylError.constructPen(hParts, hTone, rParts, rTone, scliteOutput, langSpecs)

      count = count + 1

      penaltyFile.write(newSylError.disp())
      penalties.append(newSylError.pen)

      hSylSymbol = ' '.join(hParts + [hTone])
      hSylSymbol = tuple([hSylSymbol.strip()])
      rSylSymbol = ' '.join(rParts + [rTone])
      rSylSymbol = tuple([rSylSymbol.strip()])
      sylLvlPenalties[(hSylSymbol, rSylSymbol)] = newSylError
  
  reportFile.close()
  penaltyFile.close()

  return [penalties, sylLvlPenalties]
      

#-------------------------------------------------------------------------#
def SplitTones(hSyl, rSyl):
  hParts = [part.strip() for part in hSyl.split(SUBSYL_DELIM)]
  if hParts[-1] in langSpecs[TONE]:
    hTone = hParts[-1]
    hParts = hParts[:-1]
  else:
    hTone = ''

  rParts = [part.strip() for part in rSyl.split(SUBSYL_DELIM)]
  if rParts[-1] in langSpecs[TONE]:
    rTone = rParts[-1]
    rParts = rParts[:-1]
  else:
    rTone = ''
  
  return [hParts, hTone, rParts, rTone]

#-------------------------------------------------------------------------#
def WriteTmpSylFiles(hPartsList, rPartsList):
  baseDir = os.path.dirname(os.path.abspath(__file__))
  tmpDir = os.path.join(baseDir, 'tmp')

  if not os.path.exists(tmpDir):
    os.makedirs(tmpDir);

  hypSylsPath = os.path.join(tmpDir, 'tmp_hyp_syls.txt')
  refSylsPath = os.path.join(tmpDir, 'tmp_ref_syls.txt')

  hypSylsFile = open(hypSylsPath, 'w')
  refSylsFile = open(refSylsPath, 'w')

  for i in range(len(hPartsList)):
    hParts = hPartsList[i]
    rParts = rPartsList[i]
 
    idx = i+1
    hypSylsFile.write(SUBSYL_DELIM.join(hParts) + "\t\t(" + str(idx) + ")\n") 
    refSylsFile.write(SUBSYL_DELIM.join(rParts) + "\t\t(" + str(idx) + ")\n")

  hypSylsFile.close()
  refSylsFile.close()
  return [hypSylsPath, refSylsPath]

#-------------------------------------------------------------------------#
def ComputePenalties(hyp, ref):
  for i in range(len(hyp)):
    ComputeEntryPenalties(hyp[i], ref[i])


#-------------------------------------------------------------------------#
def ComputeEntryPenalties(hyp, ref):
  [hypSyls, refSyls, penalties, sylLvlPenalties] = ComputeAllSylsErrors(hyp, ref, sclitePath, langSpecs)

  penalty = {}
  path = {}
  count = 0

  hypLen = len(hypSyls)
  refLen = len(refSyls)

  for i in range(hypLen):
    for j in range(i, hypLen+1):
      for k in range(refLen):
        for l in range(k, refLen+1):
          key = (i, j, k, l)
          penalty[key] = INF
          if j == i+1 and l == k+1:
            penalty[key] = penalties[count]
            count = count + 1
          elif j == i or l == k:
            if l > k:
              penalty[key] = (l-k) * Penalty.MAX_SYL_PEN
            if j > i:
              penalty[key] = (j-i) * Penalty.MAX_SYL_PEN
              

  for len_1 in range(1, hypLen+1):
    for len_2 in range(1, refLen+1):
      for i in range(hypLen+1-len_1):
        for m in range(refLen+1-len_2):
          for j in range(i+1, i+len_1+1):
            for n in range(m+1, m+len_2+1):
              for k in range(i, j):
                for h in range(m, n):
                  # print "i, j, m, n: " + str((i, j, m, n))
                  # print "i, k, m, h: " + str((i, k, m, h))
                  # print "k, j, h, n: " + str((k, j, h, n))
                  # print ""
                  tmp = penalty[(i, k, m, h)] + penalty[(k, j, h, n)]
                  if penalty[(i, j, m, n)] > tmp:
                    penalty[(i, j, m, n)] = tmp
                    path[(i, j, m, n)] = (k, h)
  
  report = { 'hyp': [], 'ref': [], 'pen': [], 'text': [] }
  DecodeAlignment(0, hypLen, 0, refLen, path, hypSyls, refSyls, sylLvlPenalties, report)
#   for i in range(hypLen+1):
#     for j in range(i, refLen+1):
#       for k in range(hypLen+1):
#         for l in range(k, refLen+1):
#           key = (i, j, k, l)
#           print str(key) + ": " + str(penalty[key])
#           if j == i+1 and l == k+1:
#             print str(hypSyls[i]) + "\t" + str(refSyls[k])

#-------------------------------------------------------------------------#
def DecodeAlignment(i, j, m, n, path, hypSyls, refSyls, sylLvlPenalties, report):
  label = (i, j, m, n)
  if label not in path:
    pen = 0
    hSyl = hypSyls[i:j]
    if len(hSyl) > 0:
      hSyl = tuple(hSyl)
    rSyl = refSyls[m:n]
    if len(rSyl) > 0:
      rSyl = tuple(rSyl)
    if len(hSyl) > 0 and len(rSyl) > 0:
      report['text'] == report['text'].append(sylLvlPenalties[(hSyl, rSyl)].disp())
      pen = sylLvlPenalties[(hSyl, rSyl)].pen
    else:
      if len(hSyl) == 0:
        hSyl = '*'
      if len(rSyl) == 0:
        rSyl = '*'
      pen = Penalty.MAX_SYL_PEN

      tmp = "REF:\t\t" + str(hSyl) + "\n"
      tmp = tmp + "HYP:\t\t" + str(rSyl) + "\n"
      tmp = tmp + "PENALTY:\t" + str(pen) + "\n\n"

      report['text'].append(tmp)
      report['hyp'].append(hSyl)
      report['ref'].append(rSyl)
      report['pen'].append(pen)
  else:
    (k, h) = path[label]
    DecodeAlignment(i, k, m, h, path, hypSyls, refSyls, sylLvlPenalties, report)
    DecodeAlignment(k, j, h, n, path, hypSyls, refSyls, sylLvlPenalties, report)



[hyp, ref] = getData(hypPath, refPath)
langSpecs = readLangSpecs(refLangSpecsPath)
ComputePenalties(hyp, ref)
