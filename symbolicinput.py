from helpers import isInt

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

      # Other
      'Dup': ('Dup', arg1),

      # Arithmetic operations
      'Add': ('+', arg1, arg2),
      'Sub': ('-', arg1, arg2),
      'Mul': ('*', arg1, arg2),
      'Div': ('/', arg1, arg2),
      'Mod': ('%', arg1, arg2),
      'Exp': ('**', arg1, arg2),

      # Boolean
      'Lt': ('<', arg1, arg2),
      'Gt': ('>', arg1, arg2),
      'Eq': ('==', arg1, arg2),
      'And': ('&&', arg1, arg2),
      'Or': ('||', arg1, arg2),
      'Xor': ('Xor', arg1, arg2),
      'Not': ('!', arg1),
      'IsZero': ('0 == ', arg1)
      #'Byte': ('Byte', arg1, arg2)
    }.get(op, ('bad', arg1))

  def derive(self, count):
    opChain = self.opChain
    if opChain[0] == 'id':
      count[0] += 1
      return 'x{}'.format(count[0])
      # return 'id(sym: {0}, uid: {1})'.format(self.opChain[1],self.opChain[2])

    arg1 = ''
    if isinstance(self.opChain[1], SymbolicInput):
      arg1 = opChain[1].derive(count)
    else:
      arg1 = '{}'.format(self.opChain[1])

    # If there is a second argument to process
    if len(self.opChain) > 2:
      if isinstance(self.opChain[2], SymbolicInput):
        arg2 = opChain[2].derive(count)
      else:
        arg2 = '{}'.format(self.opChain[2])
    else:
      return '({}{})'.format(self.opChain[0], arg1)

    return '({} {} {})'.format(arg1, self.opChain[0], arg2)


