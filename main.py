#!usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import evmmaps

def prettyPrint(items):
  for x in opcodes:
    print(x[0])

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

def traverseProgram(items):
  stack   = []
  memory  = []
  gasCost = 0
  i = 0
  stop = False
  while not stop:
    item = items[i]
    if item[0][:4] == "PUSH":
      # push value to stack
      stack.append(item[0][7:])
    if item[0] == "JUMP":
      i, stop = jumpToLoc(stack.pop(), items)
      continue
    if item[0] == "JUMPI":
      adr = stack.pop()
      if int(stack.pop()):
        #jump to adr
        i, stop = jumpToLoc(adr, items)
        continue
    if item[0] == "JUMPDEST":
      pass
    if item[0] == "RETURN":
      break
    #gasCost = gasCost + calculateGasCost(item[0])
    i += 1
    stop = i >= len(items)
  print(stack)

def jumpToLoc(adr, items):
  try:
    x = int(adr, 16)
  except TypeError:
    return -1, False
  return x, isValidJumpTarget(x, items)

def isValidJumpTarget(loc, items):
  return loc not in invalidTargets and\
         convert(items[loc][0])[0] == "JUMPDEST"

invalidTargets = [2]
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
  #prettyPrint(opcodes)
  traverseProgram(opcodes)

if __name__ == "__main__":
    main()

# Walking through the program
# Each step, add the gas cost (and maybe compute some formula?)
# At jmp/cmp..., split into two paths and go down both