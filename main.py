#!usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import evmmaps

def prettyPrint(list):
  for x in list:
    print(x[0])

def convert(bytecode):
  return evmmaps.byteToOP.get(bytecode, ("Unknown opcode", 0, 0))

# read input from stdin
# separate into pairs
# translate to opcodes
# run gasAnalyser
def main():
  print(len(sys.argv))
  if len(sys.argv) < 2:
    print("input the bytecode please")
    return
  bytecode  = sys.argv[1]
  charPairs = [bytecode[i:i + 2] for i in range(0, len(bytecode), 2)]
  del charPairs[0]
  i = 0
  opcodes = []
  while i < len(charPairs):
    op = list(convert(charPairs[i]))
    if op[0][0:4] == "PUSH":
      offset = int(op[0][4:])
      op[0] = op[0] + " 0x" + "".join(charPairs[i + 1:i + offset + 1])
      i += offset
    i += 1
    opcodes.append(op)
  prettyPrint(opcodes)
  #traverseProgram(opcodes)

# def traverseProgram(commands):
#   stack = []
#   for op in commands:
#     if op[0][0:4] == "PUSH":
#       # push value to stack
#       stack.append(op[0][7:])





if __name__ == "__main__":
    main()

# Walking through the program
# Each step, add the gas cost (and maybe compute some formula?)
# At jmp/cmp..., split into two paths and go down both