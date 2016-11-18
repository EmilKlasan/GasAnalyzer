import evmmaps
from math import log
debug = False

# Calculates gas cost given an op code, still need  to consider 
# operations that have costs dependent on the stack. These require
# the stack that represents the state of the program
#
# Specs for the gas function is in the ethereum yellow paper:
# CMem(new) - CMem(old) + piecewise function of gas values
#
# Note that not every opcode needs new memory, so for some opcodes
# CMem(new) - CMem(old) is just 0 and we're only concerned with
# the piecewise function

# Returns -1 if it never went into any opcode case
# TODO: Calls, SUicide, Sstore
def calculateGas(opCode, stack, memory):
  gasCost = -1

  # We consider ops with tiers first, then we move into the unranked
  # Tier costs, if the op belongs to any tiers
  if opCode in evmmaps.wzero:
    gasCost = evmmaps.gasToPrices['GZERO']
  elif opCode in evmmaps.wbase:
    gasCost += evmmaps.gasToPrices['GBASE']
  elif opCode in evmmaps.wverylow:
    gasCost += evmmaps.gasToPrices['GVERYLOW']
  elif opCode in evmmaps.wlow:
    gasCost += evmmaps.gasToPrices['GLOW']
  elif opCode in evmmaps.wmid:
    gasCost += evmmaps.gasToPrices['GMID']
  elif opCode in evmmaps.whigh:
    gasCost += evmmaps.gasToPrices['GHIGH']
  elif opCode in evmmaps.wextcode:
    gasCost += evmmaps.gasToPrices['GEXTCODE']

  if opCode == 'SLOAD':
    gasCost += evmmaps.gasToPrices['GSLOAD']
  elif opCode == 'BALANCE':
    gasCost += evmmaps.gasToPrices['GBALANCE']
  elif opCode == 'JUMPDEST':
    gasCost += evmmaps.gasToPrices['GJUMPDEST']
  elif opCode == 'BLOCKHASH':
    gasCost += evmmaps.gasToPrices['GBLOCKHASH']
  # SSTORE and SUICIDE have some nuances, will look at later

  # Ops that interact with memory
  # The gas price of the operation depending on the tier + if we need more memory
  # Not copy operations
  # first argument of calc mem gas is wrong right now, should not be using len(memory)
  # need to figure out how memory works
  elif opCode == 'MSTORE':
    gasCost += calcMemGas(len(memory), memNeeded(stack[-1], 32), 0)
  elif opCode == 'MSTORE8': # 1 byte
    gasCost += calcMemGas(len(memory), memNeeded(stack[-1], 1), 0)
  elif opCode == 'MLOAD': 
    gasCost += calcMemGas(len(memory), memNeeded(stack[-1], 32), 0)
  elif opCode == 'RETURN': 
    gasCost += calcMemGas(len(memory), memNeeded(stack[-1], stack[-2]), 0)
  # Cost for SHA3 = GSHA3 + GSHA3WORD * (s[1] / 32) + mem costs
  elif opCode == 'SHA3': 
    gasCost += (evmmaps.gasToPrices['GSHA3'] + (evmmaps.gasToPrices['GSHA3WORD'] * ((stack[-2] + 31) / 32)) +
            calcMemGas(len(memory), memNeeded(stack[-1], stack[-2]), 0))
  # For copy operations, GCOPY is taken care of in calcMemGas
  elif opCode == 'CALLDATACOPY':
    gasCost += evmmaps.gasToPrices['GVERYLOW'] + calcMemGas(len(memory), memNeeded(stack[-1], stack[-3]), stack[-3])
  elif opCode == 'CODECOPY':
    gasCost += evmmaps.gasToPrices['GVERYLOW'] + calcMemGas(len(memory), memNeeded(stack[-1], stack[-3]), stack[-3])
  elif opCode == 'EXTCODECOPY':
    gasCost += evmmaps.gasToPrices['GEXTCODE'] + calcMemGas(len(memory), memNeeded(stack[-2], stack[-4]), stack[-4])
  # Will look at Call, Callcode, DelegateCall later
  # Parse log and only do things if valid log
  elif opCode[0:3] == 'LOG':
    logNumber = 0
    try:
      logNumber = int(opCode[3])
    except ValueError:
      print 'Invalid Opcode {}'.format(opCode)
      return -1
    if logNumber in range(0,5):
      gasCost += (evmmaps.gasToPrices['GLOG'] + evmmaps.gasToPrices['GLOGDATA'] * stack[-2] 
                  + logNumber * evmmaps.gasToPrices['GLOGTOPIC'])

  elif opCode == 'CREATE':
    gasCost += evmmaps.gasToPrices['GCREATE'] + calcMemGas(len(memory), memNeeded(stack[-2], stack[-3]), 0)
  # Exp op takes into account size of exponent, also this just follows the yellowpaper, are there no
  # signed exponents in ethereum?
  elif opCode == 'EXP':
    if stack[-2] == 0:
      gasCost += evmmaps.gasToPrices['GEXP']
    elif stack[-2] > 0:
      gasCost += evmmaps.gasToPrices['GEXP'] + evmmaps.gasToPrices['GEXPBYTE'] * (1 + int(log(stack[-2], 256)))

  return gasCost


### The memory functions here are pretty similar to the java implementation of the evm
### https://github.com/ethereum/ethereumj/blob/develop/ethereumj-core/src/main/java/org/ethereum/vm/VM.java

# Given an old memory size and a new memory size, calculate the 
# amount of gas required to expand the memory. Copying operations
# also incur their own extra cost.
def calcMemGas(oldMem, newMem, copySize):
  memCost = 0

  # We calculate memory usage to the nearest word
  # Then see if we actually need to allocate anything
  # If we do, then we calculate the cost based on the function in the yellow paper
  # which is: CMem(a) = GMem * a + a ** 2 / 512
  memUse = ((newMem + 31) / 32 ) * 32
  if memUse > oldMem:
    memWords = memUse / 32
    oldMemWords = oldMem / 32
    newMemCost = (evmmaps.gasToPrices['GMEMORY'] * memWords + (memWords ** 2) / 512)
    oldMemCost = (evmmaps.gasToPrices['GMEMORY'] * oldMemWords + (oldMemWords ** 2) / 512)
    if debug:
      print 'NEW MEM COST: {}'.format(newMemCost)
      print 'OLD MEM COST: {}'.format(oldMemCost)
    memCost += newMemCost

  # Copy operations have extra costs along with memory costs, rounded up
  if copySize > 0:
    memCost += evmmaps.gasToPrices['GCOPY'] * ((copySize + 31) / 32)

  return memCost


# Pretty much the same thing as the evm's memNeeded function
# Calculates the current stack offset + the size of mem needed
# And returns a new memory size. Returns 0 if size needed is 0.
def memNeeded(offset, size):
  if debug:
    print 'OFFSET: {}\nSIZE: {}'.format(offset,size)
  return 0 if size == 0 else offset + size

