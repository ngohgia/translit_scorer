#!/usr/bin/python

import sys
import os

if __name__ == '__main__':
  try:
    script, sclitePath, outputPath, refPath, refLangSpecsPath = sys.argv
  except ValueError:
    print "translit_scorer.py\tsclitePath\toutputPath\trefPath\trefLangSpecs"
    sys.exit(1)

SYL_DELIM = '.'
SUBSYL_DELIM = ' '
ONSET = 'ONSET'
NUCLEUS = 'NUCLEUS'
CODA = 'CODA'
TONE = 'TONE'

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
  # reportFile = os.path.join(tmpDir, reportName + '.pra')
  # computeSylErrors(sylList, reportFile, oTonesFile, rTonesFile)


#-------------------------------------------------------------------------#
def computeSylErrors(reportPath, oTonesPath, rTonesPath):
  reportFile = open(reportPath, 'r')
  for line in reportFile:
    parts = [part.strip() for part in line.split()]
    if parts[0] == 'REF:':
      ref = parts[1:]
    elif parts[0] == 'HYP:':
      hyp = parts[1:]
    elif parts[0] == 'Eval:':
      score = parts[1:]
      
      

#-------------------------------------------------------------------------#
def processRefSylStruct(ref_parts, langSpecs):
  if len(ref_parts) == 3:
    self.ref[ONSET] = ref_parts[0]
    self.ref[NUCLEUS] = ref_parts[1]
    self.ref[CODA] = ref_parts[2]
  elif len(ref_parts) == 2:
    if ref_parts[0] in langSpecs[NUCLEUS]:
      self.ref[NUCLEUS] = ref_parts[0]
      self.ref[CODA] = ref_parts[1]
    if ref_parts[0] in langSpecs[ONSET]:
      self.ref[ONSET] = ref_parts[0]
      self.ref[NUCLEUS] = ref_parts[1]
  elif len(ref_parts) == 1:
    self.ref[NUCLEUS] = ref_parts[0]
  else:
    print("Reference syllable with length 0!")
    exit


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

