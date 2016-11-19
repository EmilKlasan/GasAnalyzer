#!usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import evmmaps
from math import copysign
import ctypes

############### HELPER FUNCTIONS #################

def toHex(val):
  return "%x" % val

def prettyPrint(items):
  for x in items:
    print(x)

def convert(bytecode):
  return evmmaps.byteToOP.get(bytecode, ("Unknown opcode", 0, 0))

def convertToOpcodes(items):
  opcodes = []
  i = 0
  while i < len(items):
    op = list(convert(items[i]))
    if op[0][:4] == "PUSH":
      size = int(op[0][4:])
      op[0]  = "PUSH 0x" + "".join(items[i + 1:i + size + 1])
      i += size
    i += 1
    opcodes.append(op)
  return opcodes

def getFunctionHashes(opcodes):
  funcs = []
  for x in opcodes:
    op = x[0]
    if len(op) == 15 and op[:4] == "PUSH":
      funcs.append(op[7:])
  return funcs

###################################################

arithOps = ["ADD",
            "MUL",
            "SUB",
            "DIV",
            "SDIV",
            "MOD",
            "SMOD",
            "ADDMOD",
            "MULMOD",
            "EXP",
            "SIGNEXTEND"]

boolOps = ["LT",
           "GT",
           "SLT",
           "SGT",
           "EQ",
           "ISZERO",
           "AND",
           "OR",
           "XOR",
           "NOT",
           "BYTE"]

envOps = ["ADDRESS",
          "BALANCE",
          "ORIGIN",
          "CALLER",
          "CALLVALUE",
          "CALLDATALOAD",
          "CALLDATASIZE",
          "CALLDATACOPY",
          "CODESIZE",
          "CODECOPY",
          "GASPRICE",
          "EXTCODESIZE",
          "EXTCODECOPY"]

blockOps = ["BLOCKHASH",
            "COINBASE",
            "TIMESTAMP",
            "NUMBER",
            "DIFFICULTY",
            "GASLIMIT"]

jumpOps = ["JUMP",
           "JUMPI"]

memOps = ["MLOAD",
          "MSTORE",
          "MSTORES"]

storOps = ["SLOAD",
           "SSTORE"]

terminalOps = ["STOP",
               "RETURN"]

def traverseProgram(items):
  stack   = []
  memory  = []
  storage = {}
  gasCost = 0
  stop    = False
  i       = 0
  while not stop:
    item = items[i]
    op   = item[0]
    if op in terminalOps:
      break
    elif op in arithOps:
      handleArithOps(item, stack)
    elif op in boolOps:
      handleBoolOp(item, stack)
    elif op == "SHA3":
      pass
    elif op in envOps:
      handleEnvOps(item, stack, memory)
    elif op in blockOps:
      handleBlockOps(item, stack)
    elif op in jumpOps:
      i, stop = handleJumpOps(op, stack, items)
      continue
    elif op in memOps:
      handleMemoryOps(item, stack, memory)
    elif op in storOps:
      handleStorageOps(item, stack, storage)
    elif op == "JUMPDEST":
      pass
    elif op == "POP":
      stack.pop()
    elif op == "PC":
      stack.append(i)
    elif op[:4] == "PUSH":
      # push value to stack
      stack.append(op[7:])
    elif op[:3] == "DUP":
      num = int(op[3:])
      stack.append(stack[-num])
    elif op[:4] == "SWAP":
      num         = int(op[4:])
      tmp         = stack[-num]
      stack[-num] = stack[-1]
      stack[-1]   = tmp
    elif op[:3] == "LOG":
      pass


    #gasCost = gasCost + calculateGasCost(item[0])
    i += 1
    stop = i >= len(items)
  print("Stack:")
  prettyPrint(stack)


################### JUMP OPS #####################

def handleJumpOps(op, stack, items):
  adr = stack.pop()
  out = None
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
         convert(items[loc][0])[0] == "JUMPDEST"

invalidTargets = [2]

############### ARITHMETIC OPS #################

def handleArithOps(item, stack):
  func = arithMap[item[0]]
  params = []
  for i in range(item[1]):
    params.insert(0, int(stack.pop(), 16))
  stack.append(toHex(func(params)))

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
  stack.append(toHex(func(params)))

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

def handleEnvOps(item, stack, memory):
  pass
  # func = envMap[item[0]]
  # params = []
  # for i in range(item[1]):
    # params.insert(0, int(stack.pop(), 16))
  # stack.append(toHex(func(params)))


################ BLOCK OPS #################

def handleBlockOps(item, stack):
  pass
  # func = envMap[item[0]]
  # params = []
  # for i in range(item[1]):
    # params.insert(0, int(stack.pop(), 16))
  # stack.append(toHex(func(params)))

################ MEMORY OPS ##############

def handleMemoryOps(item, stack, memory):
  pass
  # func = envMap[item[0]]
  # params = []
  # for i in range(item[1]):
    # params.insert(0, int(stack.pop(), 16))
  # stack.append(toHex(func(params)))

################ STORAGE OPS ##############

def handleStorageOps(item, stack, storage):
  pass
  # func = envMap[item[0]]
  # params = []
  # for i in range(item[1]):
    # params.insert(0, int(stack.pop(), 16))
  # stack.append(toHex(func(params)))


#############################################

############ SYMBOLIC EXECUTION #############

# EQ
# PUSH [tag] 2
# JUMPI 

def takeBothPaths(destination, condition):
  # JUMPI


#############################################

##################  MAIN  ###################

# read input from stdin
# separate into pairs
# translate to opcodes
# run gasAnalyser
def main():
  if len(sys.argv) < 2:
    print("input the bytecode please")
    return
  bytecode  = sys.argv[1]
  start = 2 if bytecode[:2] == "0x" else 0
  pairs = [bytecode[i:i + 2] for i in range(start, len(bytecode), 2)]
  opcodes = convertToOpcodes(pairs)
  #prettyPrint([opcodes[i][0] for i in range(len(opcodes))])
  functions = getFunctionHashes(opcodes)
  print("Functions:")
  prettyPrint(functions)
  traverseProgram(opcodes)

if __name__ == "__main__":
    main()

# Walking through the program
# Each step, add the gas cost (and maybe compute some formula?)
# At jmp/cmp..., split into two paths and go down both