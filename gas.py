import evmmaps

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
  if opCode == 'CREATE':
    return evmmaps.gasToPrices['GCREATE']
  elif opCode == 'JUMPDEST':
    return evmmaps.gasToPrices['GJUMPDEST']
  elif opCode == 'SLOAD':
    return evmmaps.gasToPrices['GSLOAD']
  elif opCode in evmmaps.wzero:
    return evmmaps.gasToPrices['GZERO']
  elif opCode in evmmaps.wbase:
    return evmmaps.gasToPrices['GBASE']
  elif opCode in evmmaps.wverylow:
    return evmmaps.gasToPrices['GVERYLOW']
  elif opCode in evmmaps.wlow:
    return evmmaps.gasToPrices['GLOW']
  elif opCode in evmmaps.wmid:
    return evmmaps.gasToPrices['GMID']
  elif opCode in evmmaps.whigh:
    return evmmaps.gasToPrices['GHIGH']
  elif opCode in evmmaps.wextcode:
    return evmmaps.gasToPrices['GEXTCODE']
  elif opCode == 'BALANCE':
    return evmmaps.gasToPrices['GBALANCE']
  elif opCode == 'BLOCKHASH':
    return evmmaps.gasToPrices['GBLOCKHASH']
  # for now
  else:
    return 0

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
    memCost += ((evmmaps.gasToPrices['GMEMORY'] * memWords + (memWords ** 2) / 512) - 
                (evmmaps.gasToPrices['GMEMORY'] * oldMemWords + (oldMemWords ** 2) / 512))



  return memCost


# Pretty much the same thing as the evm's memNeeded function
# Calculates the current stack offset + the size of mem needed
# And returns a new memory size. Returns 0 if size needed is 0.
def memNeeded(offset, size):
  return 0 if size == 0 else offset + size

