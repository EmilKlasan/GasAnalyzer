import helpers
import ophandlers
import oplists

class ExecutionPath:
  def __init__(self, opcodes, functions, stack = [], memory = [], storage = {}, symbols = []):
    self.opcodes   = opcodes,
    self.functions = functions,
    self.stack     = stack,
    self.memory    = memory,
    self.storage   = storage,
    self.symbols   = symbols

  def traverse(self):
    items   = self.opcodes
    stack   = self.stack
    memory  = self.memory
    storage = self.storage
    gasCost = 0
    stop    = False
    i       = 0
    while not stop:
      item = items[i]
      op   = item[0]
      if op in oplists.terminalOps:
        break
      elif op in oplists.arithOps:
        ophandlers.handleArithOps(item, stack)
      elif op in oplists.boolOps:
        ophandlers.handleBoolOp(item, stack)
      elif op == "SHA3":
        pass
      elif op in oplists.envOps:
        pass# ophandlers.handleEnvOps(item, stack, memory)
      elif op in oplists.blockOps:
        ophandlers.handleBlockOps(item, stack)
      elif op in oplists.jumpOps:
        result  = ophandlers.handleJumpOps(op, stack, items)
        if result[0] != -1:
          i, stop = result
          continue
      elif op in oplists.memOps:
        ophandlers.handleMemoryOps(item, stack, memory)
      elif op in oplists.storOps:
        ophandlers.handleStorageOps(item, stack, storage)
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
    helpers.prettyPrint(stack)
    print("Memory:")
    helpers.prettyPrint(memory)
    print("Storage:")
    helpers.prettyPrint(storage)
