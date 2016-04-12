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
ONSET = 'CONSO'
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
def computeScliteScore(hyp, ref, outputDir):
  os.system(sclitePath + " -r " + ref + \
          " -h " + hyp + \
          " -i wsj -o pra -O " + outputDir)

#--------------------------------------------------------------------------#
def computeAllSylErrors(output, ref, sclitePath, langSpecs):
  sylErrorDict = {}
  
  baseDir = os.path.dirname(os.path.abspath(__file__))
  tmpDir = os.path.join(baseDir, 'tmp')

  tmpOutput = os.path.join(tmpDir, 'tmp_output_syls.txt')
  tmpRef    = os.path.join(tmpDir, 'tmp_ref_syls.txt')
  outputTones = os.path.join(tmpDir, 'tmp_output_tones.txt')
  refTones = os.path.join(tmpDir, 'tmp_ref_tones.txt')

  if os.path.exists(tmpOutput):
    os.remove(tmpOutput)
  if os.path.exists(tmpRef):
    os.remove(tmpRef)
  if os.path.exists(outputTones):
    os.remove(outputTones)
  if os.path.exists(refTones):
    os.remove(refTones)

  for i in range(len(output)):
    outputEntry = output[i];
    refEntry = ref[i];

    outputSyls = [part.strip() for part in outputEntry.split(SYL_DELIM)]
    refSyls = [part.strip() for part in refEntry.split(SYL_DELIM)]

    idx = 1
    for oSyl in outputSyls:
      for rSyl in refSyls:
        writeTmpSylFiles(idx, oSyl, rSyl, langSpecs)
        idx = idx + 1

  computeScliteScore(tmpOutput, tmpRef, tmpDir)

#-------------------------------------------------------------------------#
def writeTmpSylFiles(idx, oSyl, rSyl, langSpecs):
  baseDir = os.path.dirname(os.path.abspath(__file__))
  tmpDir = os.path.join(baseDir, 'tmp')

  if not os.path.exists(tmpDir):
    os.makedirs(tmpDir);
 
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

  outputSylsFile = open(os.path.join(tmpDir, 'tmp_output_syls.txt'), 'a')
  refSylsFile = open(os.path.join(tmpDir, 'tmp_ref_syls.txt'), 'a')
  outputTonesFile = open(os.path.join(tmpDir, 'tmp_output_tones.txt'), 'a')
  refTonesFile = open(os.path.join(tmpDir, 'tmp_ref_tones.txt'), 'a')
  
  outputSylsFile.write(SUBSYL_DELIM.join(oParts) + "\t\t(" + str(idx) + ")\n") 
  refSylsFile.write(SUBSYL_DELIM.join(rParts) + "\t\t(" + str(idx) + ")\n")
  outputTonesFile.write(oTone + "\n") 
  refTonesFile.write(rTone + "\n")

  outputSylsFile.close()
  refSylsFile.close()

[output, ref] = getData(outputPath, refPath)
langSpecs = readLangSpecs(refLangSpecsPath)
computeAllSylErrors(output, ref, sclitePath, langSpecs)

