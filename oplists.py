arithOps = ["ADD",
            "MUL",
            "SUB",
            "DIV",
            "SDIV",
            "MOD",
            "SMOD",
            "ADDMOD",
            "MULMOD",
            "EXP",
            "SIGNEXTEND"]

boolOps = ["LT",
           "GT",
           "SLT",
           "SGT",
           "EQ",
           "ISZERO",
           "AND",
           "OR",
           "XOR",
           "NOT",
           "BYTE"]

envOps = ["ADDRESS",
          "BALANCE",
          "ORIGIN",
          "CALLER",
          "CALLVALUE",
          "CALLDATALOAD",
          "CALLDATASIZE",
          "CALLDATACOPY",
          "CODESIZE",
          "CODECOPY",
          "GASPRICE",
          "EXTCODESIZE",
          "EXTCODECOPY"]

blockOps = ["BLOCKHASH",
            "COINBASE",
            "TIMESTAMP",
            "NUMBER",
            "DIFFICULTY",
            "GASLIMIT"]

jumpOps = ["JUMP",
           "JUMPI"]

memOps = ["MLOAD",
          "MSTORE",
          "MSTORES"]

storOps = ["SLOAD",
           "SSTORE"]

terminalOps = ["STOP",
               "RETURN"]