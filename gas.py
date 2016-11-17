import evmmaps
debug = True

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

def calculateGas(opCode, stack):
  return {
    # The simple ones that are pretty much constant
    'STOP': evmmaps.gasToPrices['GZERO'],
    'SLOAD': evmmaps.gasToPrices['GSLOAD'],
    'BALANCE': evmmaps.gasToPrices['GBALANCE'],
    # SSTORE and SUICIDE have some nuances, will look at later

    # Ops that interact with memory
    # The gas price of the operation depending on the tier + if we need more memory
    # Not copy operations
    # first argument of calc mem gas is wrong right now, should not be using len(stack)
    # need to figure out how memory works
    'MSTORE': (evmmaps.gasToPrices['GVERYLOW'] + calcMemGas(len(stack), memNeeded(stack[-1], 32), 0)),
    'MSTORE8': (evmmaps.gasToPrices['GVERYLOW'] + calcMemGas(len(stack), memNeeded(stack[-1], 1), 0)), # 1 byte
    'MLOAD': (evmmaps.gasToPrices['GVERYLOW'] + calcMemGas(len(stack), memNeeded(stack[-1], 32), 0)),
    'RETURN': (evmmaps.gasToPrices['GZERO'] + calcMemGas(len(stack), memNeeded(stack[-1], stack[-2]), 0)),
    # Cost for SHA3 = GSHA3 + GSHA3WORD * (s[1] / 32) + mem costs
    'SHA3': (evmmaps.gasToPrices['GSHA3'] + (evmmaps.gasToPrices['GSHA3WORD'] * ((stack[-2] + 31) / 32)) +
            calcMemGas(len(stack), memNeeded(stack[-1], stack[-2]), 0))

  }.get(opCode, 0)

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

