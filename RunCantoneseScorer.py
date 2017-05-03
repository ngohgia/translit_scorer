#!/usr/bin/python

import sys
import os
import os.path as op
import subprocess

sclitePath = '/Users/ngohgia/Work/transliteration/utilities/sclite'

# -------------------------- MANDARIN ------------------------------ #
rootDir = os.getcwd()
dataDir = op.join(rootDir, 'sample', 'cantonese')
hypPath = op.join(dataDir, 'cantonese_sample.hyp')
refPath = op.join(dataDir, 'cantonese_sample.ref')
refLangSpecs = op.join(rootDir, 'CantoneseLang', 'cantonese_lang_specs.txt')
reportDir = op.join(dataDir, 'reports')
if not os.path.exists(reportDir):
  os.mkdir(reportDir)
reportName = 'cantonese_translit_report'

subprocess.Popen(['python', 'TranslitScorer.py', hypPath, refPath, reportDir, reportName, refLangSpecs, sclitePath]).communicate()
