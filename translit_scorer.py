#!/usr/bin/python

import sys
import os
from SylError import SylError
from Constants import Constants

if __name__ == '__main__':
  try:
    script, sclitePath, outputPath, refPath, refLangSpecsPath = sys.argv
  except ValueError:
    print "translit_scorer.py\tsclitePath\toutputPath\trefPath\trefLangSpecs"
    sys.exit(1)

SYL_DELIM = '.'
SUBSYL_DELIM = ' '
ONSET = Constants.ONSET
NUCLEUS = Constants.NUCLEUS
CODA = Constants.CODA
TONE = Constants.TONE

REF = Constants.REF
HYP = Constants.HYP
EVAL = Constants.EVAL

#---------------------------------------------------------------------------#
def readLangSpecs(specPath):
  langSpecs = {}
  specFile = open(specPath, 'r')
  for line in specFile:
    parts = [part.strip() for part in line.split()]
    langSpecs[parts[0]] = parts[1:]
  return langSpecs

#---------------------------------------------------------------------------#
def getData(outputPath, refPath):
  output = []
  ref = []

  outputFile = open(outputPath, 'r');
  for line in outputFile:
    output.append(line.strip())
  outputFile.close()

  refFile = open(refPath, 'r');
  for line in refFile:
    ref.append(line.strip())
  refFile.close()

  if len(output) != len(ref):
    print "Number of output and reference entries do not match"
    exit(1)

  return [output, ref];

#--------------------------------------------------------------------------#
def ComputeScliteScore(hyp, ref, outputDir):
  reportName = 'syl_errors'
  os.system(sclitePath + " -r " + ref + \
          " -h " + hyp + \
          " -i wsj -o pra -O " + outputDir + \
          " -n " + reportName)
  return os.path.join(outputDir, reportName + '.pra')

#--------------------------------------------------------------------------#
def computeAllSylErrors(output, ref, sclitePath, langSpecs):
  sylList = []
  
  baseDir = os.path.dirname(os.path.abspath(__file__))
  tmpDir = os.path.join(baseDir, 'tmp')

  oPartsList = []
  rPartsList = []
  oTonesList = []
  rTonesList = []


  for i in range(len(output)):
    outputEntry = output[i];
    refEntry = ref[i];

    outputSyls = [part.strip() for part in outputEntry.split(SYL_DELIM)]
    refSyls = [part.strip() for part in refEntry.split(SYL_DELIM)]

    idx = 1
    for oSyl in outputSyls:
      for rSyl in refSyls:
        entry = (oSyl, rSyl)
        sylList.append(entry)

        [oParts, oTone, rParts, rTone] = SplitTones(oSyl, rSyl)
        oPartsList.append(oParts)
        oTonesList.append(oTone)
        rPartsList.append(rParts)
        rTonesList.append(rTone)
        idx = idx + 1

  [tmpOutput, tmpRef] = WriteTmpSylFiles(oPartsList, rPartsList)
  reportPath = ComputeScliteScore(tmpOutput, tmpRef, tmpDir)
  computeSylErrors(reportPath, oPartsList, oTonesList, rPartsList, rTonesList, langSpecs)


#-------------------------------------------------------------------------#
def computeSylErrors(reportPath, oPartsList, oTonesList, rPartsList, rTonesList, langSpecs):
  reportFile = open(reportPath, 'r')

  tmpDir = "/".join(reportPath.split("/")[:-1])
  penaltyFile = open(os.path.join(tmpDir, 'penalty_report.txt'), 'w')
  count = 0

  REF = Constants.REF
  HYP = Constants.HYP
  EVAL = Constants.EVAL

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

      oParts = oPartsList[count]
      oTone  = oTonesList[count]
      rParts = rPartsList[count]
      rTone  = rTonesList[count]
      newSylError.constructPen(oParts, oTone, rParts, rTone, scliteOutput, langSpecs)

      count = count + 1

      penaltyFile.write(newSylError.disp())
  
  reportFile.close()
  penaltyFile.close()
      

#-------------------------------------------------------------------------#
def SplitTones(oSyl, rSyl):
  oParts = [part.strip() for part in oSyl.split(SUBSYL_DELIM)]
  if oParts[-1] in langSpecs[TONE]:
    oTone = oParts[-1]
    oParts = oParts[:-1]
  else:
    oTone = ''

  rParts = [part.strip() for part in rSyl.split(SUBSYL_DELIM)]
  if rParts[-1] in langSpecs[TONE]:
    rTone = rParts[-1]
    rParts = rParts[:-1]
  else:
    rTone = ''
  
  return [oParts, oTone, rParts, rTone]

#-------------------------------------------------------------------------#
def WriteTmpSylFiles(oPartsList, rPartsList):
  baseDir = os.path.dirname(os.path.abspath(__file__))
  tmpDir = os.path.join(baseDir, 'tmp')

  if not os.path.exists(tmpDir):
    os.makedirs(tmpDir);

  outputSylsPath = os.path.join(tmpDir, 'tmp_output_syls.txt')
  refSylsPath = os.path.join(tmpDir, 'tmp_ref_syls.txt')

  outputSylsFile = open(outputSylsPath, 'w')
  refSylsFile = open(refSylsPath, 'w')

  for i in range(len(oPartsList)):
    oParts = oPartsList[i]
    rParts = rPartsList[i]
 
    idx = i+1
    outputSylsFile.write(SUBSYL_DELIM.join(oParts) + "\t\t(" + str(idx) + ")\n") 
    refSylsFile.write(SUBSYL_DELIM.join(rParts) + "\t\t(" + str(idx) + ")\n")

  outputSylsFile.close()
  refSylsFile.close()
  return [outputSylsPath, refSylsPath]

[output, ref] = getData(outputPath, refPath)
langSpecs = readLangSpecs(refLangSpecsPath)
computeAllSylErrors(output, ref, sclitePath, langSpecs)

