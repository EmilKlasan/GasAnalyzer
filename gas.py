import evmmaps

# Calculates gas cost given an op code, currently using 
def calculateGas(str opCode):
  if opCode in evmmaps.wzero:
    return evmmaps.gasToPrices['GZERO']
  else if opCode in evmmaps.wbase:
    return evmmaps.gasToPrices['GBASE']
  else if opCode in evmmaps.wverylow:
    return evmmaps.gasToPrices['GVERYLOW']
  else if opCode in evmmaps.wlow:
    return evmmaps.gasToPrices['GLOW']
  else if opCode in evmmaps.wmid:
    return evmmaps.gasToPrices['GMID']
  else if opCode in evmmaps.whigh:
    return evmmaps.gasToPrices['GHIGH']
  else if opCode in evmmaps.wextcode:
    return evmmaps.gasToPrices['GEXTCODE']
  # for now
  else
    return 0