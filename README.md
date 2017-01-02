# [WIP] Transliteration Scorer

Run `python translit_scorer.py   hypPath   refPath  reportDir  reportName  refLangSpecs  sclitePath`

Example:

`python translit_scorer.py sample/sample.out sample/sample.vie sample/ report VieLang/vie_lang_specs.txt ~/sclite/sclite`

This command will score the hypothesis in `sample/sample.out` against `sample/sample.vie` and save the reports into `sample/` directory using Sclite executable at `~/sclite/sclite` 

There will be two reports `sample/report.summary.txt` and `sample/report.full.csv`.
