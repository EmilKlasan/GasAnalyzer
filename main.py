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
  start          = 2 if bytecode[:2] == "0x" else 0
  pairs          = [bytecode[i:i + 2] for i in range(start, len(bytecode), 2)]
  opcodes   = helpers.convertToOpcodes(pairs)
  functions = helpers.getFunctionHashes(opcodes)
  exPath    = ExecutionPath(opcodes, functions)
  exPath.traverse()

if __name__ == "__main__":
    main()