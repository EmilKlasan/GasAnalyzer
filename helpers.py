
import evmmaps

############### HELPER FUNCTIONS #################

def isInt(val):
  try:
    int(val)
    return True
  except (ValueError, AttributeError, TypeError):
    return False

def toHex(val):
  return "%x" % val

def prettyPrint(items):
  for x in items:
    print(x)

def convert(bytecode):
  return evmmaps.byteToOP.get(bytecode, ("Unknown opcode", 0, 0))

def convertToOpcodes(items):
  opcodes = {}
  i = 0
  lastIndex = -1;
  while i < len(items):
    # print(i)
    op = list(convert(items[i]))
    if op[0][:4] == "PUSH":
      size = int(op[0][4:])
      op[0]  = "PUSH 0x" + "".join(items[i + 1:i + size + 1])
      i += size
    if lastIndex > 0:
      opcodes[lastIndex].append(i)
    opcodes[i] = op
    lastIndex = i
    i += 1
  opcodes[lastIndex].append(-1)
  return opcodes

def getFunctionHashes(opcodes):
  funcs = []
  for i in opcodes:
    x = opcodes[i]
    op = x[0]
    if len(op) == 15 and op[:4] == "PUSH":
      funcs.append(op[7:])
  return funcs