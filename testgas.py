import gas
import evmmaps

# This function tests if opCode is considered in calculateGas
# Will print the opcodes that are not considered
def testOpCodes():
  testStack = [0,0,0,0]
  testMem = [0,0,0,0]
  results = []
  print 'The following OpCodes were not considered in calculateGas:'
  for x in evmmaps.byteToOP:
    n = gas.calculateGas(evmmaps.byteToOP[x][0], testStack, testMem)
    results.append((evmmaps.byteToOP[x][0], n != -1))
    if n == -1:
      print evmmaps.byteToOP[x][0]
  return results