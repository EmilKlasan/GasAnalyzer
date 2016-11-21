class SymbolicInput:

  # id of sym, operation that made it, the argument that came with the operation
  # if the sym is made with identity operation, so that means that it came from
  # an EVM envop or storage op, then the op is 'id' and the arg1 will be the
  # user input that made it
  def __init__(self, symId, op, arg1, arg2 = None):
    self.symId = symId
    self.opChain = self.generateOp(op, arg1, arg2)

  def getId(self):
    return self.symId

  def generateOp(self, op, arg1, arg2):
    return {
      'id': ('id', self.symId, arg1),
      '+': ('+', arg1, arg2),
      '-': ('-', arg1, arg2),
      '*': ('*', arg1, arg2),
      '/': ('/', arg1, arg2)
    }.get(op, ('bad', arg1))

  def derive(self):
    opChain = self.opChain
    if opChain[0] == 'id':
      return 'id(sym: {0}, uid: {1})'.format(self.opChain[1],self.opChain[2 ])

    arg1 = ''
    if isinstance(self.opChain[1], SymbolicInput):
      arg1 = opChain[1].derive()
    else:
      arg1 = '{}'.format(self.opChain[1])

    if isinstance(self.opChain[2], SymbolicInput):
      arg2 = opChain[1].derive()
    else:
      arg2 = '{}'.format(self.opChain[2])

    return '{}({}, {})'.format(self.opChain[0], arg1, arg2)


