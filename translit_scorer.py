#!/usr/bin/python

import sys
import os

if __name__ == '__main__':
  try:
    script, sclitePath, outputPath, refPath = sys.argv
  except ValueError:
    print "translit_scorer.py\tsclitPath\toutputPath\trefPath"
    sys.exit(1)

SYL_DELIM = '.'

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
def computeAllSylErrors(output, ref, sclitePath):
  sylErrorDict = {}
  
  baseDir = os.path.dirname(os.path.abspath(__file__))
  tmpDir = os.path.join(baseDir, 'tmp')

  if os.path.exists(tmpDir):
    os.remove(os.path.join(tmpDir, 'tmp_output_syls.txt'))
    os.remove(os.path.join(tmpDir, 'tmp_ref_syls.txt'))

  for i in range(len(output)):
    outputEntry = output[i];
    refEntry = ref[i];

    outputSyls = [part.strip() for part in outputEntry.split(SYL_DELIM)]
    refSyls = [part.strip() for part in refEntry.split(SYL_DELIM)]

    idx = 1
    for oSyl in outputSyls:
      for rSyl in refSyls:
        entry = (oSyl, rSyl)
        writeTmpSylFiles(idx, oSyl, rSyl)
        idx = idx + 1

#-------------------------------------------------------------------------#
def writeTmpSylFiles(idx, oSyl, rSyl):
  baseDir = os.path.dirname(os.path.abspath(__file__))
  tmpDir = os.path.join(baseDir, 'tmp')

  if not os.path.exists(tmpDir):
    os.makedirs(tmpDir);
  
  outputSylsFile = open(os.path.join(tmpDir, 'tmp_output_syls.txt'), 'a')
  refSylsFile = open(os.path.join(tmpDir, 'tmp_ref_syls.txt'), 'a')
  
  outputSylsFile.write(oSyl + "\t\t(" + str(idx) + ")\n") 
  refSylsFile.write(rSyl + "\t\t(" + str(idx) + ")\n")

  outputSylsFile.close()
  refSylsFile.close()

[output, ref] = getData(outputPath, refPath)
computeAllSylErrors(output, ref, sclitePath)

