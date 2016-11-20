
import evmmaps

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