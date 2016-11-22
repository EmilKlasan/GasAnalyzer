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
      # Represents the base symbol, used when reading user input
      'id': ('id', self.symId, arg1),

      # Arithmetic operations
      'Add': ('Add', arg1, arg2),
      'Sub': ('Sub', arg1, arg2),
      'Mul': ('Mul', arg1, arg2),
      'Div': ('Div', arg1, arg2),
      'Mod': ('Mod', arg1, arg2),
      'Exp': ('Exp', arg1, arg2),

      # Boolean
      'Lt': ('Lt', arg1, arg2),
      'Gt': ('Gt', arg1, arg2),
      'Eq': ('Eq', arg1, arg2),
      'Iszero': ('Eq', arg1, 0),
      'And': ('And', arg1, arg2),
      'Or': ('Or', arg1, arg2),
      'Xor': ('Xor', arg1, arg2),
      'Not': ('Not', arg1),
      'Byte': ('Byte', arg1, arg2)
    }.get(op, ('bad', arg1))

  def derive(self):
    opChain = self.opChain
    if opChain[0] == 'id':
      return 'id(sym: {0}, uid: {1})'.format(self.opChain[1],self.opChain[2])

    arg1 = ''
    if isinstance(self.opChain[1], SymbolicInput):
      arg1 = opChain[1].derive()
    else:
      arg1 = '{}'.format(self.opChain[1])

    # If there is a second argument to process
    if len(self.opChain[2]) > 2:
      if isinstance(self.opChain[2], SymbolicInput):
        arg2 = opChain[2].derive()
      else:
        arg2 = '{}'.format(self.opChain[2])
    else:
      return '{}({})'.format(self.opChain[0], arg1)

    return '{}({}, {})'.format(self.opChain[0], arg1, arg2)


