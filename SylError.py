class SylError
  ONSET = 'ONSET'
  NUCLEUS = 'NUCLEUS'
  CODA = 'CODA'

  CORRECT = 'C'
  SUB     = 'S'
  DEL     = 'D'
  INS     = 'I'

  def __init__(self):
    self.ref = {}
    self.hyp = {}

    self.onset   = CORRECT
    self.nucleus = CORRECT
    self.coda    = CORRECT

  def compute_pen(ref_syl, hyp_syl, syl_score, ref_tone, hyp_tone):
