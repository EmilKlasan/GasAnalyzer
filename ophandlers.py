
import helpers
import ctypes
from math import copysign

################### JUMP OPS #####################

def handleJumpOps(op, stack, items):
  adr = stack.pop()
  out = (-1, False)
  if op == "JUMP" or (op == "JUMPI" and int(stack.pop(), 16)):
    #jump to adr
    out = jumpToLoc(adr, items)
  return out

def jumpToLoc(adr, items):
  try:
    x = int(adr, 16)
  except TypeError:
    return -1, False
  return x, not isValidJumpTarget(x, items)

def isValidJumpTarget(loc, items):
  return loc not in invalidTargets and\
         helpers.convert(items[loc][0])[0] == "JUMPDEST"

invalidTargets = [2]

############### ARITHMETIC OPS #################

def handleArithOps(item, stack):
  func = arithMap[item[0]]
  params = []
  for i in range(item[1]):
    params.insert(0, int(stack.pop(), 16))
  stack.append(helpers.toHex(func(params)))

def signedDiv(params):
  x = params[0]
  y = params[1]
  if not y:
    return y
  elif x == -(2**255) and y == -1:
    return -(2**255)
  else:
    return copysign(abs(x / y), x / y)

def signedMod(params):
  x = params[0]
  y = params[1]
  if y:
    return copysign(abs(x) % abs(y), x)
  return y

# need to check if this works
def signExtend(params):
  x = params[0]
  i = params[1]
  sign_bit = 1 << (i - 1)
  return (x & (sign_bit - 1)) - (x & sign_bit)

arithMap = {
  "ADD":        lambda params: params[0] + params[1],
  "MUL":        lambda params: params[0] * params[1],
  "SUB":        lambda params: params[0] - params[1],
  "DIV":        lambda params: params[0] / params[1] if params[1] else 0,
  "MOD":        lambda params: params[0] % params[1] if params[1] else 0,
  "ADDMOD":     lambda params: (params[0] + params[1]) % params[2] if params[2] else 0,
  "MULMOD":     lambda params: (params[0] * params[1]) % params[2] if params[2] else 0,
  "EXP":        lambda params: params[0] ** params[1],
  "SDIV":       signedDiv,
  "SMOD":       signedMod,
  "SIGNEXTEND": signExtend
}

############### BOOLEAN OPS #################

def makeUnsigned256(i):
    return ctypes.c_ubyte(i).value

def handleBoolOp(item, stack):
  func = boolMap[item[0]]
  params = []
  for i in range(item[1]):
    params.insert(0, int(stack.pop(), 16))
  stack.append(helpers.toHex(func(params)))

boolMap = {
  "LT":     lambda params: makeUnsigned256(params[0]) < makeUnsigned256(params[1]),
  "GT":     lambda params: makeUnsigned256(params[0]) > makeUnsigned256(params[1]),
  "SLT":    lambda params: params[0] < params[1],
  "SGT":    lambda params: params[0] > params[1],
  "EQ":     lambda params: params[0] == params[1],
  "ISZERO": lambda params: not params[0],
  "AND":    lambda params: params[0] & params[1],
  "OR":     lambda params: params[0] | params[1],
  "XOR":    lambda params: params[0] ^ params[1],
  "NOT":    lambda params: params[0],
  "BYTE":   lambda params: (params[1] >> (8 * params[0])) & 0xFF
}

################ ENVIRONMENTAL OPS ##############

# def handleEnvOps(item, stack, memory):
#   func = envMap[item[0]]
#   #params = []
#   for i in range(item[1]):
#     params.insert(0, int(stack.pop(), 16))
#   if item[2] == 1:
#     x = SymbolicInput(symId)
#     x -= 1
#     stack.append(symId)
  #stack.append(helpers.toHex(func(params)))


################ BLOCK OPS #################

def handleBlockOps(item, stack):
  pass
  # func = envMap[item[0]]
  # params = []
  # for i in range(item[1]):
    # params.insert(0, int(stack.pop(), 16))
  # stack.append(helpers.toHex(func(params)))

################ MEMORY OPS ##############

def handleMemoryOps(item, stack, memory):
  pass
  # func = envMap[item[0]]
  # params = []
  # for i in range(item[1]):
    # params.insert(0, int(stack.pop(), 16))
  # stack.append(helpers.toHex(func(params)))

################ STORAGE OPS ##############

def handleStorageOps(item, stack, storage):
  pass
  # func = envMap[item[0]]
  # params = []
  # for i in range(item[1]):
    # params.insert(0, int(stack.pop(), 16))
  # stack.append(helpers.toHex(func(params)))


#############################################