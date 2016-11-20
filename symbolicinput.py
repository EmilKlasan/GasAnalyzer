class SymbolicInput:
  def __init__(self, symId, constraints = []):
    self.symId = symId
    self.constraints = constraints

  def getConstraints(self):
    return self.constraints

  def getId(self):
    return self.symId