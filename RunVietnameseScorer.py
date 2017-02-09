#!/usr/bin/python

import sys
import os
import os.path as op
import subprocess

sclitePath = '/Users/ngohgia/Work/transliteration/utilities/sclite'

# -------------------------- VIETNAMESE ------------------------------ #
rootDir = os.getcwd()
dataDir = op.join(rootDir, 'sample', 'vietnamese')
hypPath = op.join(dataDir, 'vietnamese_sample.hyp')
refPath = op.join(dataDir, 'vietnamese_sample.ref')
refLangSpecs = op.join(rootDir, 'VieLang', 'vie_lang_specs.txt')
reportDir = op.join(dataDir, 'reports')
if not os.path.exists(reportDir):
  os.mkdir(reportDir)
reportName = 'vietnamese_translit_report'

subprocess.Popen(['python', 'TranslitScorer.py', hypPath, refPath, reportDir, reportName, refLangSpecs, sclitePath]).communicate()
