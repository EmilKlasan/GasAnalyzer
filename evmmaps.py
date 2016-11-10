# File containing relevant gas mappings, opcode mappings, and gas sets

# map of EVM bytecode to tuple of (opcode, a, b) where
# a = # of items removed from stack
# b = # of items placed on stack
# Reference is appendix H of http://gavwood.com/Paper.pdf

byteToOP = {
  # Stops and arithmetic
  '00':('STOP', 0, 0),
  '01':('ADD', 2, 1),
  '02':('MUL', 2, 1),
  '03':('SUB', 2, 1),
  '04':('DIV', 2, 1),
  '05':('SDIV', 2, 1),
  '06':('MOD', 2, 1),
  '07':('SMOD', 2, 1),
  '08':('ADDMOD', 3, 1),
  '09':('MULMOD', 3, 1),
  '0a':('EXP', 2, 1),
  '0b':('SIGNEXTEND', 2, 1),
  
  # Comparisons and Bitwise Operations
  '10':('LT', 2, 1),
  '11':('GT', 2, 1),
  '12':('SLT', 2, 1),
  '13':('SGT', 2, 1),
  '14':('EQ', 2, 1),
  '15':('ISZERO', 1, 1),
  '16':('AND', 2, 1),
  '17':('OR', 2, 1),
  '18':('XOR', 2, 1),
  '19':('NOT', 1, 1),
  '1a':('BYTE', 2, 1),

  # SHA3
  '20':('SHA3', 2, 1),

  # Environmental Information
  '30':('ADDRESS', 0, 1),
  '31':('BALANCE', 1, 1),
  '32':('ORIGIN', 0, 1),
  '33':('CALLER', 0, 1),
  '34':('CALLVALUE', 0, 1),
  '35':('CALLDATALOAD', 1, 1),
  '36':('CALLDATASIZE', 0, 1),
  '37':('CALLDATACOPY', 3, 0),
  '38':('CODESIZE', 0, 1),
  '39':('CODECOPY', 3, 0),
  '3a':('GASPRICE', 0, 1),
  '3b':('EXTCODESIZE', 1, 1),
  '3c':('EXTCODECOPY', 4, 0),

  # Block Information
  '40':('BLOCKHASH', 1, 1),
  '41':('COINBASE', 0, 1),
  '42':('TIMESTAMP', 0, 1),
  '43':('NUMBER', 0, 1),
  '44':('DIFFICULTY', 0, 1),
  '45':('GASLIMIT', 0, 1),

  # Stack, Memory, Storage, Flow Operations
  '50':('POP', 1, 0),
  '51':('MLOAD', 1, 1),
  '52':('MSTORE', 2, 0),
  '53':('MSTORES', 2, 0),
  '54':('SLOAD', 1, 1),
  '55':('SSTORE', 2, 0),
  '56':('JUMP', 1, 0),
  '57':('JUMP1', 2, 0),
  '58':('PC', 0, 1),
  '59':('MSIZE', 0, 1),
  '5a':('GAS', 0, 1),
  '5b':('JUMPDEST', 0, 0),

  # Pushes
  '60':('PUSH1', 0, 1),
  '61':('PUSH2', 0, 1),
  '62':('PUSH3', 0, 1),
  '63':('PUSH4', 0, 1),
  '64':('PUSH5', 0, 1),
  '65':('PUSH6', 0, 1),
  '66':('PUSH7', 0, 1),
  '67':('PUSH8', 0, 1),
  '68':('PUSH9', 0, 1),
  '69':('PUSH10', 0, 1),
  '6a':('PUSH11', 0, 1),
  '6b':('PUSH12', 0, 1),
  '6c':('PUSH13', 0, 1),
  '6d':('PUSH14', 0, 1),
  '6e':('PUSH15', 0, 1),
  '6f':('PUSH16', 0, 1),
  '70':('PUSH17', 0, 1),
  '71':('PUSH18', 0, 1),
  '72':('PUSH19', 0, 1),
  '73':('PUSH20', 0, 1),
  '74':('PUSH21', 0, 1),
  '75':('PUSH22', 0, 1),
  '76':('PUSH23', 0, 1),
  '77':('PUSH24', 0, 1),
  '78':('PUSH25', 0, 1),
  '79':('PUSH26', 0, 1),
  '7a':('PUSH27', 0, 1),
  '7b':('PUSH28', 0, 1),
  '7c':('PUSH29', 0, 1),
  '7d':('PUSH30', 0, 1),
  '7e':('PUSH31', 0, 1),
  '7f':('PUSH32', 0, 1),

  # Duplication Operations
  '80':('DUP1', 1, 2),
  '81':('DUP2', 2, 3),
  '82':('DUP3', 3, 4),
  '83':('DUP4', 4, 5),
  '84':('DUP5', 5, 6),
  '85':('DUP6', 6, 7),
  '86':('DUP7', 7, 8),
  '87':('DUP8', 8, 9),
  '88':('DUP9', 9, 10),
  '89':('DUP10', 10, 11),
  '8a':('DUP11', 11, 12),
  '8b':('DUP12', 12, 13),
  '8c':('DUP13', 13, 14),
  '8d':('DUP14', 14, 15),
  '8e':('DUP15', 15, 16),
  '8f':('DUP16', 16, 17),

  # Swap Operations
  '90':('SWAP1', 2, 2),
  '91':('SWAP2', 3, 3),
  '92':('SWAP3', 4, 4),
  '93':('SWAP4', 5, 5),
  '94':('SWAP5', 6, 6),
  '95':('SWAP6', 7, 7),
  '96':('SWAP7', 8, 8),
  '97':('SWAP8', 9, 9),
  '98':('SWAP9', 10, 10),
  '99':('SWAP10', 11, 11),
  '9a':('SWAP11', 12, 12),
  '9b':('SWAP12', 13, 13),
  '9c':('SWAP13', 14, 14),
  '9d':('SWAP14', 15, 15),
  '9e':('SWAP15', 16, 16),
  '9f':('SWAP16', 17, 17),

  # Log Operations
  'a0':('LOG0', 2, 0),
  'a1':('LOG1', 3, 0),
  'a2':('LOG2', 4, 0),
  'a3':('LOG3', 5, 0),
  'a4':('LOG4', 6, 0),

  # System Operations
  'f0':('CREATE', 3, 1),
  'f1':('CALL', 7, 1),
  'f2':('CALLCODE', 7, 1),
  'f3':('RETURN', 2, 0),
  'f4':('DELEGATECALL', 6, 1),
  'ff':('SUICIDE', 1, 0)
}



# Gas sets - basically which tier of gas does each opcode belong in

wzero = set(['STOP','RETURN'])
wbase = set(['ADDRESS', 'ORIGIN', 'CALLER', 'CALLVALUE', 'CALLDATASIZE', 'CODESIZE',
       'GASPRICE', 'COINBASE', 'TIMESTAMP', 'NUMBER', 'DIFFICULTY', 'GASLIMIT',
       'POP', 'PC', 'MSIZE', 'GAS'])

wverylow = set(['ADD', 'SUB', 'NOT', 'LT', 'GT', 'SLT', 'SGT', 'EQ', 'ISZERO', 'AND',
        'OR', 'XOR', 'BYTE', 'CALLDATALOAD', 'MLOAD', 'MSTORE', 'MSTORES'])
for i in range(1,33):
  wverylow.add('PUSH'+str(i))
  if i <= 16:
    wverylow.add('DUP'+str(i))
    wverylow.add('SWAP'+str(i))

wlow = set(['MUL', 'DIV', 'SDIV', 'MOD', 'SMOD', 'SIGNEXTEND'])
wmid = set(['ADDMOD', 'MULMOD', 'JUMP'])
whigh = set(['JUMP1'])
wextcode = set(['EXTCODESIZE'])


# Gas prices - cost per operation is a function of these prices
gasToPrices = {
  'GZERO':0,
  'GBASE':2,
  'GVERYLOW':3,
  'GLOW':5,
  'GMID':8,
  'GHIGH':10,
  'GEXTCODE':700,
  'GBALANCE':400,
  'GSLOAD':200,
  'GJUMPDEST':1,
  'GSSET':20000,
  'GRESET':5000,
  'RSCLEAR':15000,
  'RSUICIDE':24000,
  'GSUICIDE':5000,
  'GCREATE':32000,
  'GCODEDEPOSIT':200,
  'GCALL':700,
  'GCALLVALUE':9000,
  'GCALLSTIPEND':2300,
  'GNEWACCOUNT':25000,
  'GEXP':10,
  'GEXPBYTE':10,
  'GMEMORY':3,
  'GTXCREATE':32000,
  'GTXDATAZERO':4,
  'GTXDATANONZERO':68,
  'GTRANSACTION':21000,
  'GLOG':375,
  'GLOGDATA':8,
  'GLOGTOPIC':375,
  'GSHA3':30,
  'GSHA3WORD':6,
  'GCOPY':3,
  'GBLOCKHASH':20
}