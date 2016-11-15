import evmmaps

# Calculates gas cost given an op code, still need  to consider 
# operations that have costs dependent on the stack
def calculateGas(opCode):
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
