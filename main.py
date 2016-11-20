#!usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import helpers
from program import Program
from symbolicinput import SymbolicInput

# id for symbolic input, decrements from -1 since everything
# else on the stack will be positive for the EVM
symId = -1
symMap = {}
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
  p         = Program(bytecode)
  p.traverse()

if __name__ == "__main__":
    main()