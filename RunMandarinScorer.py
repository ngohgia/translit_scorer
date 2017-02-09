#!/usr/bin/python

import sys
import os
import os.path as op
import subprocess

sclitePath = '/Users/ngohgia/Work/transliteration/utilities/sclite'

# -------------------------- MANDARIN ------------------------------ #
rootDir = os.getcwd()
dataDir = op.join(rootDir, 'sample', 'mandarin')
hypPath = op.join(dataDir, 'mandarin_sample.hyp')
refPath = op.join(dataDir, 'mandarin_sample.ref')
refLangSpecs = op.join(rootDir, 'MandarinLang', 'mandarin_lang_specs.txt')
reportDir = op.join(dataDir, 'reports')
if not os.path.exists(reportDir):
  os.mkdir(reportDir)
reportName = 'mandarin_translit_report'

subprocess.Popen(['python', 'TranslitScorer.py', hypPath, refPath, reportDir, reportName, refLangSpecs, sclitePath]).communicate()
