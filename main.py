#!usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import helpers
from executionpath import ExecutionPath

# id for symbolic input, decrements from -1 since everything
# else on the stack will be positive for the EVM

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
  start     = 2 if bytecode[:2] == "0x" else 0
  pairs     = [bytecode[i:i + 2] for i in range(start, len(bytecode), 2)]
  opcodes   = helpers.convertToOpcodes(pairs)
  functions = helpers.getFunctionHashes(opcodes)
  exPath    = ExecutionPath(opcodes, functions)
  paths     = [exPath]
  steps     = 0;
  pathSymbols = []
  while paths and steps < 500:
    path = paths.pop()
    outList, p = path.traverse()
    for x in outList:
      paths.append(x)
    if not outList:
      pathSymbols.append(p)
    steps += 1

  pathNum = 1
  for path in pathSymbols:
    symbs = path.symbols
    gasCost = path.gasCost
    count = [0]
    print('For path {}'.format(pathNum))
    print('Gas Cost {}'.format(gasCost))
    for x in symbs:
      print 'x{}: {}'.format(count[0] + 1, symbs[x].derive(count))
    print ''
    pathNum += 1

if __name__ == "__main__":
    main()