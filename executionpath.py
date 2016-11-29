import helpers
import ophandlers
import oplists
import gas
from copy import deepcopy

class ExecutionPath:
  def __init__(self, opcodes,
                     functions,
                     stack    = [],
                     memory   = [],
                     storage  = {},
                     symbols  = {},
                     userIn   = [],
                     instrPtr = 1,
                     symId    = [-1],
                     gasCost  = 0):
    self.opcodes   = opcodes
    self.functions = functions
    self.stack     = stack
    self.memory    = memory
    self.storage   = storage
    self.symbols   = symbols
    self.userIn    = userIn  # list of symbols that directly represent user input
    self.instrPtr  = instrPtr # instruction pointer
    self.symId     = symId
    self.gasCost   = gasCost

  def takeJumpPath(self, pair):
    # negate isZero, set new symbol, check/return for jumpdest
    self.instrPtr = pair[1][0]
    ophandlers.makeJump(pair[0], self.symbols, self.symId)

  def traverse(self):
    stop    = False
    while not stop:
      try:
        item = self.opcodes[self.instrPtr]
      except KeyError:
        print('exiting on error (key {} invalid)'.format(self.instrPtr))
        break
      op   = item[0]
      if op in oplists.terminalOps:
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        print('normal exit')
        break
      elif op in oplists.arithOps:
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        ophandlers.handleArithOps(item,
                                  self.stack,
                                  self.symbols,
                                  self.symId)
      elif op in oplists.boolOps:
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        ophandlers.handleBoolOp(item,
                                self.stack,
                                self.symbols,
                                self.symId)
      elif op == "SHA3":
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        pass
      elif op in oplists.envOps:
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        ophandlers.handleEnvOps(item,
                                self.stack,
                                self.memory,
                                self.symbols,
                                self.userIn,
                                self.symId,
                                self.instrPtr)
      elif op in oplists.blockOps:
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        ophandlers.handleBlockOps(item,
                                  self.stack,
                                  self.symbols)
      elif op in oplists.jumpOps:
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        result = ophandlers.handleJumpOps(op,
                                          self.stack,
                                          self.opcodes,
                                          self.symbols,
                                          self.symId)
        if result[0] != -1 and result[1] != -1:
          self.instrPtr, stop = result
          continue
        elif result[1] == -1:
          # symbolic, need to split
          # pass path-specific parameters by value
          ep1 = ExecutionPath(self.opcodes,
                              self.functions,
                              self.stack[:],
                              self.memory[:],
                              deepcopy(self.storage),
                              deepcopy(self.symbols),
                              self.userIn[:],
                              self.instrPtr,
                              self.symId,
                              self.gasCost)
          ep1.takeJumpPath(result[0])
          self.instrPtr = item[-1]
          # print("splitting")
          return ([self, ep1], self)
      elif op in oplists.memOps:
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        ophandlers.handleMemoryOps(item,
                                   self.stack,
                                   self.memory,
                                   self.symbols)
      elif op in oplists.storOps:
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        ophandlers.handleStorageOps(item,
                                    self.stack,
                                    self.storage,
                                    self.symbols,
                                    self.userIn)
      elif op == "JUMPDEST":
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        pass
      elif op == "POP":
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        self.stack.pop()
      elif op == "PC":
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        self.stack.append(i)
      elif op[:4] == "PUSH":
        # push value to stack
        self.gasCost += gas.calculateGas(op[:4], self.stack, self.memory)
        self.stack.append(int(op[7:], 16))
      elif op[:3] == "DUP":
        self.gasCost += gas.calculateGas(op[:3], self.stack, self.memory)
        on = ophandlers.handleDupOp(op,
                                    self.symbols,
                                    self.stack,
                                    self.symId)
        self.stack.append(on)
      elif op[:4] == "SWAP":
        self.gasCost += gas.calculateGas(op[:4], self.stack, self.memory)
        num         = int(op[4:])
        tmp         = self.stack[-num]
        self.stack[-num] = self.stack[-1]
        self.stack[-1]   = tmp
      elif op[:3] == "LOG":
        self.gasCost += gas.calculateGas(op, self.stack, self.memory)
        pass

      # print(self)
      print item
      print("Stack:")
      helpers.prettyPrint(self.stack)
      print(self.gasCost)
      for sym in self.symbols:
        print(self.symbols[sym].derive([0]))
      # print("Symbols")
      # for x in self.symbols:
      #   print ''
      #   print 'symbol {}:'.format(x)
      #   print self.symbols[x].derive()
      # print ''

      #gasCost = gasCost + calculateGasCost(item[0])
      self.instrPtr = item[-1]
      stop = self.instrPtr == -1
    # print("Stack:")
    # helpers.prettyPrint(self.stack)
    # print("Memory:")
    # helpers.prettyPrint(self.memory)
    # print("Storage:")
    # helpers.prettyPrint(self.storage)

    # for x in self.symbols:
    #   print ''
    #   print 'symbol {}:'.format(x)
    #   print self.symbols[x].derive()
    return ([], self)

