# Intcode CPU
import sys
import os

from termcolor import colored


program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,5,19,23,2,9,23,27,1,6,27,31,1,31,9,35,2,35,10,39,1,5,39,43,2,43,9,47,1,5,47,51,1,51,5,55,1,55,9,59,2,59,13,63,1,63,9,67,1,9,67,71,2,71,10,75,1,75,6,79,2,10,79,83,1,5,83,87,2,87,10,91,1,91,5,95,1,6,95,99,2,99,13,103,1,103,6,107,1,107,5,111,2,6,111,115,1,115,13,119,1,119,2,123,1,5,123,0,99,2,0,14,0]

TEST = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,11,91,225,1002,121,77,224,101,-6314,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1102,74,62,225,1102,82,7,224,1001,224,-574,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1101,28,67,225,1102,42,15,225,2,196,96,224,101,-4446,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1101,86,57,225,1,148,69,224,1001,224,-77,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1101,82,83,225,101,87,14,224,1001,224,-178,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,38,35,225,102,31,65,224,1001,224,-868,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1101,57,27,224,1001,224,-84,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1101,61,78,225,1001,40,27,224,101,-89,224,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,226,224,1002,223,2,223,1006,224,329,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,344,101,1,223,223,1107,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,1007,226,226,224,102,2,223,223,1006,224,374,101,1,223,223,7,677,677,224,102,2,223,223,1005,224,389,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,404,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,419,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,434,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,464,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,479,101,1,223,223,1007,226,677,224,1002,223,2,223,1006,224,494,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,524,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,539,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,554,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,569,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,677,224,102,2,223,223,1005,224,599,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,614,101,1,223,223,8,226,226,224,102,2,223,223,1006,224,629,101,1,223,223,108,226,677,224,102,2,223,223,1005,224,644,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,659,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226]

BOOST = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,3,0,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,33,1003,1101,0,23,1002,1102,1,557,1022,1102,1,24,1010,1102,1,22,1014,1101,470,0,1027,1102,38,1,1001,1102,1,21,1012,1102,1,1,1021,1101,0,26,1018,1101,0,827,1024,1101,690,0,1029,1101,0,473,1026,1102,1,27,1015,1101,695,0,1028,1101,822,0,1025,1102,1,35,1019,1102,1,30,1000,1101,0,39,1013,1101,25,0,1016,1101,28,0,1006,1102,1,36,1004,1101,34,0,1011,1101,31,0,1017,1101,0,0,1020,1101,29,0,1009,1102,1,554,1023,1102,32,1,1007,1101,37,0,1008,1101,20,0,1005,109,5,2101,0,0,63,1008,63,20,63,1005,63,203,4,187,1106,0,207,1001,64,1,64,1002,64,2,64,109,-4,2107,21,4,63,1005,63,227,1001,64,1,64,1105,1,229,4,213,1002,64,2,64,109,4,2108,37,3,63,1005,63,251,4,235,1001,64,1,64,1106,0,251,1002,64,2,64,109,12,21101,40,0,-5,1008,1012,38,63,1005,63,275,1001,64,1,64,1105,1,277,4,257,1002,64,2,64,109,-14,21108,41,41,10,1005,1013,299,4,283,1001,64,1,64,1105,1,299,1002,64,2,64,109,5,1202,-4,1,63,1008,63,36,63,1005,63,321,4,305,1106,0,325,1001,64,1,64,1002,64,2,64,109,-3,2108,38,-1,63,1005,63,345,1001,64,1,64,1106,0,347,4,331,1002,64,2,64,109,-8,1201,4,0,63,1008,63,40,63,1005,63,367,1105,1,373,4,353,1001,64,1,64,1002,64,2,64,109,20,1205,4,391,4,379,1001,64,1,64,1106,0,391,1002,64,2,64,109,5,1205,-2,407,1001,64,1,64,1106,0,409,4,397,1002,64,2,64,109,-15,2102,1,-3,63,1008,63,36,63,1005,63,431,4,415,1106,0,435,1001,64,1,64,1002,64,2,64,109,-6,1202,6,1,63,1008,63,31,63,1005,63,459,1001,64,1,64,1105,1,461,4,441,1002,64,2,64,109,28,2106,0,-2,1105,1,479,4,467,1001,64,1,64,1002,64,2,64,109,-14,21107,42,41,-4,1005,1011,499,1001,64,1,64,1106,0,501,4,485,1002,64,2,64,109,8,1206,-3,515,4,507,1105,1,519,1001,64,1,64,1002,64,2,64,109,-29,2101,0,6,63,1008,63,33,63,1005,63,539,1105,1,545,4,525,1001,64,1,64,1002,64,2,64,109,30,2105,1,-1,1106,0,563,4,551,1001,64,1,64,1002,64,2,64,109,5,1206,-8,579,1001,64,1,64,1106,0,581,4,569,1002,64,2,64,109,-31,1201,3,0,63,1008,63,38,63,1005,63,607,4,587,1001,64,1,64,1106,0,607,1002,64,2,64,109,11,21101,43,0,4,1008,1013,43,63,1005,63,633,4,613,1001,64,1,64,1106,0,633,1002,64,2,64,109,-10,2107,22,3,63,1005,63,651,4,639,1106,0,655,1001,64,1,64,1002,64,2,64,109,26,21102,44,1,-8,1008,1017,44,63,1005,63,681,4,661,1001,64,1,64,1105,1,681,1002,64,2,64,109,-3,2106,0,6,4,687,1105,1,699,1001,64,1,64,1002,64,2,64,109,-3,21108,45,43,0,1005,1019,715,1105,1,721,4,705,1001,64,1,64,1002,64,2,64,109,-25,1207,9,32,63,1005,63,737,1105,1,743,4,727,1001,64,1,64,1002,64,2,64,109,18,21107,46,47,3,1005,1015,761,4,749,1106,0,765,1001,64,1,64,1002,64,2,64,109,-3,2102,1,-3,63,1008,63,31,63,1005,63,789,1001,64,1,64,1105,1,791,4,771,1002,64,2,64,109,-5,1208,-4,30,63,1005,63,813,4,797,1001,64,1,64,1105,1,813,1002,64,2,64,109,28,2105,1,-8,4,819,1106,0,831,1001,64,1,64,1002,64,2,64,109,-30,1207,0,24,63,1005,63,853,4,837,1001,64,1,64,1106,0,853,1002,64,2,64,109,16,21102,47,1,-7,1008,1011,45,63,1005,63,873,1105,1,879,4,859,1001,64,1,64,1002,64,2,64,109,-21,1208,5,26,63,1005,63,899,1001,64,1,64,1105,1,901,4,885,4,64,99,21102,27,1,1,21102,915,1,0,1106,0,922,21201,1,69417,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1106,0,922,21201,1,0,-1,21201,-2,-3,1,21101,0,957,0,1105,1,922,22201,1,-1,-2,1105,1,968,22102,1,-2,-2,109,-3,2106,0,0]

BOOST = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,3,0,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,33,1003,1101,0,23,1002,1102,1,557,1022,1102,1,24,1010,1102,1,22,1014,1101,470,0,1027,1102,38,1,1001,1102,1,21,1012,1102,1,1,1021,1101,0,26,1018,1101,0,827,1024,1101,690,0,1029,1101,0,473,1026,1102,1,27,1015,1101,695,0,1028,1101,822,0,1025,1102,1,35,1019,1102,1,30,1000,1101,0,39,1013,1101,25,0,1016,1101,28,0,1006,1102,1,36,1004,1101,34,0,1011,1101,31,0,1017,1101,0,0,1020,1101,29,0,1009,1102,1,554,1023,1102,32,1,1007,1101,37,0,1008,1101,20,0,1005,109,5,2101,0,0,63,1008,63,20,63,1005,63,203,4,187,1106,0,207,1001,64,1,64,1002,64,2,64,109,-4,2107,21,4,63,1005,63,227,1001,64,1,64,1105,1,229,4,213,1002,64,2,64,109,4,2108,37,3,63,1005,63,251,4,235,1001,64,1,64,1106,0,251,1002,64,2,64,109,12,21101,40,0,-5,1008,1012,38,63,1005,63,275,1001,64,1,64,1105,1,277,4,257,1002,64,2,64,109,-14,21108,41,41,10,1005,1013,299,4,283,1001,64,1,64,1105,1,299,1002,64,2,64,109,5,1202,-4,1,63,1008,63,36,63,1005,63,321,4,305,1106,0,325,1001,64,1,64,1002,64,2,64,109,-3,2108,38,-1,63,1005,63,345,1001,64,1,64,1106,0,347,4,331,1002,64,2,64,109,-8,1201,4,0,63,1008,63,40,63,1005,63,367,1105,1,373,4,353,1001,64,1,64,1002,64,2,64,109,20,1205,4,391,4,379,1001,64,1,64,1106,0,391,1002,64,2,64,109,5,1205,-2,407,1001,64,1,64,1106,0,409,4,397,1002,64,2,64,109,-15,2102,1,-3,63,1008,63,36,63,1005,63,431,4,415,1106,0,435,1001,64,1,64,1002,64,2,64,109,-6,1202,6,1,63,1008,63,31,63,1005,63,459,1001,64,1,64,1105,1,461,4,441,1002,64,2,64,109,28,2106,0,-2,1105,1,479,4,467,1001,64,1,64,1002,64,2,64,109,-14,21107,42,41,-4,1005,1011,499,1001,64,1,64,1106,0,501,4,485,1002,64,2,64,109,8,1206,-3,515,4,507,1105,1,519,1001,64,1,64,1002,64,2,64,109,-29,2101,0,6,63,1008,63,33,63,1005,63,539,1105,1,545,4,525,1001,64,1,64,1002,64,2,64,109,30,2105,1,-1,1106,0,563,4,551,1001,64,1,64,1002,64,2,64,109,5,1206,-8,579,1001,64,1,64,1106,0,581,4,569,1002,64,2,64,109,-31,1201,3,0,63,1008,63,38,63,1005,63,607,4,587,1001,64,1,64,1106,0,607,1002,64,2,64,109,11,21101,43,0,4,1008,1013,43,63,1005,63,633,4,613,1001,64,1,64,1106,0,633,1002,64,2,64,109,-10,2107,22,3,63,1005,63,651,4,639,1106,0,655,1001,64,1,64,1002,64,2,64,109,26,21102,44,1,-8,1008,1017,44,63,1005,63,681,4,661,1001,64,1,64,1105,1,681,1002,64,2,64,109,-3,2106,0,6,4,687,1105,1,699,1001,64,1,64,1002,64,2,64,109,-3,21108,45,43,0,1005,1019,715,1105,1,721,4,705,1001,64,1,64,1002,64,2,64,109,-25,1207,9,32,63,1005,63,737,1105,1,743,4,727,1001,64,1,64,1002,64,2,64,109,18,21107,46,47,3,1005,1015,761,4,749,1106,0,765,1001,64,1,64,1002,64,2,64,109,-3,2102,1,-3,63,1008,63,31,63,1005,63,789,1001,64,1,64,1105,1,791,4,771,1002,64,2,64,109,-5,1208,-4,30,63,1005,63,813,4,797,1001,64,1,64,1105,1,813,1002,64,2,64,109,28,2105,1,-8,4,819,1106,0,831,1001,64,1,64,1002,64,2,64,109,-30,1207,0,24,63,1005,63,853,4,837,1001,64,1,64,1106,0,853,1002,64,2,64,109,16,21102,47,1,-7,1008,1011,45,63,1005,63,873,1105,1,879,4,859,1001,64,1,64,1002,64,2,64,109,-21,1208,5,26,63,1005,63,899,1001,64,1,64,1105,1,901,4,885,4,64,99,21102,27,1,1,21102,915,1,0,1106,0,922,21201,1,69417,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1106,0,922,21201,1,0,-1,21201,-2,-3,1,21101,0,957,0,1105,1,922,22201,1,-1,-2,1105,1,968,22102,1,-2,-2,109,-3,2106,0,0]

larger_example = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

position_mode_eq_eight = [3,9,8,9,10,9,4,9,99,-1,8]
position_mode_lt_eight = [3,9,7,9,10,9,4,9,99,-1,8]

position_mode_jmp_test = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
# position_mode_jmp_test = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
position_mode_jmp_test   = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]

immediate_mode_eq_eight = [3,3,1108,-1,8,3,4,3,99]
immediate_mode_lt_eight = [3,3,1107,-1,8,3,4,3,99]

immediate_mode_jmp_test = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

test_vectors = [
    {'in':  [1,0,0,0,99],
     'out': [2,0,0,0,99]},
    {'in':  [2,3,0,3,99],
     'out': [2,3,0,6,99]},
    {'in':  [2,4,4,5,99,0],
     'out': [2,4,4,5,99,9801]},
    {'in':  [1,1,1,4,99,5,6,0,99],
     'out': [30,1,1,4,2,5,6,0,99]},

    {'name': "Read Input",
     'in':     [3,4,99,0,0],
     'out':    [3,4,99,0,42],
     'input':  [42]},
    {'name': "Write Output",
     'in':     [4,4,99,0,42],
     'out':    [4,4,99,0,42],
     'output': [42]},
    {'in':     [3,0,4,0,99],
     'out':    [42,0,4,0,99],
     'input':  [42],
     'output': [42]},
    {'in':     [1002,4,3,4,33],
     'out':    [1002,4,3,4,99]},

    {'name': "Larger Example 8",
     'in':     larger_example,
     'input':  [8],
     'output': [1000],
    },
    {'name': "Larger Example 7",
     'in':     larger_example,
     'input':  [7],
     'output': [999],
    },
    {'name': "Larger Example 9",
     'in':     larger_example,
     'input':  [9],
     'output': [1001],
    },

    {'in': position_mode_eq_eight, 'input':  [7], 'output': [0] },
    {'in': position_mode_eq_eight, 'input':  [8], 'output': [1] },
    {'in': position_mode_eq_eight, 'input':  [9], 'output': [0] },
    
    {'in': position_mode_lt_eight, 'input':  [7], 'output': [1], 'name': "position mode 7 < 8?" },
    {'in': position_mode_lt_eight, 'input':  [8], 'output': [0], 'name': "position mode 8 < 8?" },

    
    {'in': list(position_mode_jmp_test), 'input':  [-1], 'output': [1], 'name': "jmp 1" },
    {'in': list(position_mode_jmp_test), 'input':  [1], 'output': [1], 'name': "jmp 2" },
    {'in': list(position_mode_jmp_test), 'input':  [0], 'output': [0], 'name': "jmp 3" },


    {'name': 'TEST',
     'in': list(TEST),
     'input': [5],
     'output': [15724522],
    },
    
    {'in': immediate_mode_eq_eight, 'input':  [7], 'output': [0] },
    {'in': immediate_mode_eq_eight, 'input':  [8], 'output': [1] },
    {'in': immediate_mode_eq_eight, 'input':  [9], 'output': [0] },

    {'in': immediate_mode_lt_eight, 'input':  [7], 'output': [1] },
    {'in': immediate_mode_lt_eight, 'input':  [8], 'output': [0] },

    {'in': list(immediate_mode_jmp_test), 'input':  [0], 'output': [0] },
    {'in': list(immediate_mode_jmp_test), 'input':  [-1], 'output': [1] },
    {'in': list(immediate_mode_jmp_test), 'input':  [1], 'output': [1] },

    # Day 9 tests
    {'name': 'Quine',
     'in':  [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99],
     'output': [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99],
    },
    {'in': [1102,34915192,34915192,7,4,7,99,0],
     'output': [1219070632396864],
    },
    {'in': [104,1125899906842624,99],
     'output': [1125899906842624],
    },
    {'name': 'BOOST self test',
     'in': list(BOOST),
     'input': [1],
     'output': [3598076521],
    },
]

POSITION_MODE = "0"
IMMEDIATE_MODE = "1"
RELATIVE_MODE = "2"

DEBUG = os.getenv('DEBUG', False)

def debug(msg):
    if DEBUG:
        print(msg)

class Parameter:
    def __init__(self, name=None, kind=None):
        self.name = name
        self.kind = kind
        self.mode = "Position"
        self.value = None
        self.address = None

    def __repr__(self):
        return f"name: {self.name} kind: {self.kind} mode: {self.mode} value: {self.value}"

class IntOp:
    def __init__(self):
        self.opcode = None
        self.parameters = []
        self.param = {}
        self.cpu = None
        self.name = type(self).__name__
        self.setup()

    def setup(self):
        pass

    def operation(self):
        pass

    def __repr__(self):
        return(f"{self.name}")


class Add(IntOp):
    def setup(self):
        self.opcode = 1
        self.parameters = [
            Parameter(name="A"),
            Parameter(name="B"),
            Parameter(name="Target", kind="Output"),
            ]
    def op(self):
        self.cpu.memory[self.param["Target"]] = self.param["A"] + self.param["B"]
    

class Multiply(IntOp):
    def setup(self):
        self.opcode = 2
        self.parameters = [
            Parameter(name="A"),
            Parameter(name="B"),
            Parameter(name="Target", kind="Output"),
            ]
    def op(self):
        self.cpu.memory[self.param["Target"]] = self.param["A"] * self.param["B"]


class Read(IntOp):
    def setup(self):
        self.opcode = 3
        self.parameters = [
            Parameter(name="Target", kind="Output")
            ]
    def op(self):
        self.cpu.memory[self.param["Target"]] = self.cpu.data_in.pop(0)

class Write(IntOp):
    def setup(self):
        self.opcode = 4
        self.parameters = [
            Parameter(name="Target", kind="Output")
            ]
    def op(self):
        output = self.cpu.memory[self.param["Target"]]
        if self.cpu.show_output:
            print(output)
        self.cpu.data_out.append(output)
        self.cpu.pause = True

class JumpTrue(IntOp):
    def setup(self):
        self.opcode = 5
        self.parameters = [
            Parameter(name="Test"),
            Parameter(name="Location"),
        ]
    def op(self):
        if self.param["Test"] != 0:
            self.cpu.instruction_pointer = self.param["Location"]


class JumpFalse(IntOp):
    def setup(self):
        self.opcode = 6
        self.parameters = [
            Parameter(name="Test"),
            Parameter(name="Location"),
        ]
    def op(self):
        if self.param["Test"] == 0:
            self.cpu.instruction_pointer = self.param["Location"]
        debug(f"JumpFalse instruction pointer set to {self.cpu.instruction_pointer} params {self.param}")
        
        
class LessThan(IntOp):
    def setup(self):
        self.opcode = 7
        self.parameters = [
            Parameter(name="A"),
            Parameter(name="B"),
            Parameter(name="Answer", kind="Output"),
        ]
    def op(self):
        value = 0
        if self.param["A"] < self.param["B"]:
            value = 1
        self.cpu.memory[self.param["Answer"]] = value
        
        
class Equal(IntOp):
    def setup(self):
        self.opcode = 8
        self.parameters = [
            Parameter(name="A"),
            Parameter(name="B"),
            Parameter(name="Answer", kind="Output"),
            ]
    def op(self):
        value = 0
        if self.param["A"] == self.param["B"]:
            value = 1
        target = self.param["Answer"]
        debug(f"Writing {value} to {target}")
        self.cpu.memory[target] = value

class IncrementRelative(IntOp):
    def setup(self):
        self.opcode = 9
        self.parameters = [
            Parameter(name="RelativeOffset"),
            ]
    def op(self):
        self.cpu.relative_base += self.param["RelativeOffset"]

class Halt(IntOp):
    def setup(self):
        self.opcode = 99
        self.parameters = []
    def op(self):
        self.cpu.running = False
        

class IntcodeCPU:
    def __init__(self):
        self.instructions = [
            Add(),
            Multiply(),
            Read(),
            Write(),
            JumpTrue(),
            JumpFalse(),
            LessThan(),
            Equal(),
            IncrementRelative(),
            Halt(),
        ]
        self.opcodes = {}
        for instruction in self.instructions:
            self.opcodes[instruction.opcode] = instruction
        self.reset()


    def reset(self):
        self.pause = False
        self.data_in = []
        self.data_out = []
        self.instruction_pointer = 0
        self.memory = []
        self.relative_base = 0
        self.running = True
        self.show_output = False
        self.token_pointer = 0


    @property
    def output(self):
        return self.data_out


    # FIXME: This can be removed
    def explain_opcode(self):
        def id(kind):
            if kind == "0":
                return "Positional"
            elif kind == "1":
                return "Immediate"
            elif kind == "2":
                return "Relative"
            else:
                return "Unknown"
        raw_opcode = self.tokens[self.token_pointer]['value']
        abcde = str(raw_opcode)
        while(len(abcde) < 5):
            abcde = "0" + abcde
        opcode = int(abcde[3:])
        mode = [
            id(abcde[2]),
            id(abcde[1]),
            id(abcde[0]),
        ]
        return opcode, mode

    def load_tokens(self):
        found = []
        for address, value in enumerate(self.memory):
            found.append({"address": address, "value": value})
        self.tokens = found
    
    def explain(self):
        if not DEBUG:
            return
        self.load_tokens()
        parsed = []
        self.token_pointer = 0
        while(self.token_pointer < len(self.tokens)):
            # FIXME: Clean this up to be more in line with go()
            opcode, mode = self.explain_opcode()
            # print(f"token: {self.token_pointer} opcode: {opcode}")
            if opcode in self.opcodes:
                instruction = self.tokens[self.token_pointer].copy()
                instruction["name"] = self.opcodes[opcode].name
                instruction["type"] = "Instruction"
                parsed.append(instruction.copy())
                parameters = self.opcodes[opcode].parameters
                for parameter_number, parameter in enumerate(parameters):
                    offset = self.token_pointer + parameter_number + 1
                    # FIXME
                    if offset >= len(self.tokens):
                        continue
                    token = self.tokens[offset].copy()
                    token["type"] = "Parameter"
                    if "mode" not in token:
                        token["mode"] = parameter.mode
                    if "name" not in token:
                        token["name"] = parameter.name
                    # parsed.append({**token, **parameter})
                    parsed.append(token)

                offset = 1 + len(self.opcodes[opcode].parameters)
                self.token_pointer += offset
            else:
                instruction = self.tokens[self.token_pointer].copy()
                instruction["name"] = ""
                instruction["type"] = "Unknown"
                parsed.append(instruction)
                self.token_pointer += 1


        print(f"Input:         {self.data_in}")
        print(f"Output:        {self.data_out}")
        print(f"Relative Base: {self.relative_base}")
        print("Ip Adr Value      h Name       Extra")
        print("-- --- ---------- - ---------- --------------------")
        for i in parsed:
            # print(i)
            type_hint = " "
            extra = ""
            type_hint = "?"
            if "mode" not in i:
                type_hint = "_"
            elif i["mode"] == "Immediate":
                type_hint = "="
            elif i["mode"] == "Positional" and i["value"] <= len(self.tokens):
                type_hint = "~"
                extra = "({})".format(self.tokens[i["value"]]["value"])
            elif i["mode"] == "Relative" and i["value"] <= len(self.tokens):
                type_hint = "!"
                extra = "<{}>".format(self.tokens[i["value"]]["value"])
            # elif i["type"] == "Unknown":
            #     type_hint = "?"
            if "kind" in i and i["kind"] == "Output" and i["value"] <= len(self.tokens):
                loc = i["value"]
                if loc >= len(self.tokens):
                    extra = "=> [??]"
                else:
                    extra = "=> [{}]".format(self.tokens[loc]["value"])
            i["type_hint"] = type_hint
            i["extra"] = extra

            # print(i)

            i["prefix"] = ""
            if i["address"] == self.instruction_pointer:
                i["prefix"] = ">"

            if "name" not in i:
                i["name"] = "UHHH"
                
            out = "{prefix: >2} {address: >3} {value: >10} {type_hint} {name: <10} {extra}".format(**i)
            if i["type"] == "Instruction":
                print(colored(out, "grey", attrs=["bold"]))
            elif i["type"] == "Parameter":
                print(colored(out, "green"))
            elif i["type"] == "Unknown":
                print(colored(out, "red", attrs=["bold"]))
            else:
                print(out)
                print(i)
        print("-- --- ---------- - ---------- --------------------")
        

    def load_instruction(self):
        def id(kind):
            if kind == "0":
                return "Position"
            elif kind == "1":
                return "Immediate"
            elif kind == "2":
                return "Relative"
            else:
                return "Unknown"
        raw_opcode = self.memory[self.instruction_pointer]
        abcde = str(raw_opcode)
        while(len(abcde) < 5):
            abcde = "0" + abcde
        opcode = int(abcde[3:])
        if opcode in self.opcodes:
            instruction = self.opcodes[opcode]
        else:
            print(f"Unrecognized opcode: {opcode}")
            sys.exit(100)

        self.instruction_pointer += 1
        mode = [id(x) for x in list(abcde[0:3])]
        for index, parameter in enumerate(instruction.parameters):
            address = 0
            parameter.mode = mode.pop()
            if parameter.mode == "Immediate":
                address = self.instruction_pointer
            elif parameter.mode == "Position":
                address = self.memory[self.instruction_pointer]
            elif parameter.mode == "Relative":
                value = self.memory[self.instruction_pointer]
                address = self.relative_base + value
            else:
                print("Unable to determine mode")
                sys.exit(100)
            if address >= len(self.memory):
                size = address - len(self.memory) + 2
                debug(f"Extending memory by: {size}")
                padding = [0 for i in range(size)]
                self.memory += padding
            if parameter.kind == "Output":
                instruction.param[parameter.name] = address
            else:
                instruction.param[parameter.name] = self.memory[address]
            self.instruction_pointer += 1
        return instruction


    def run(self, memory):
        self.memory = memory
        return self.go()


    def go(self):
        while(self.running):
            self.explain()
            instruction = self.load_instruction()
            instruction.cpu = self
            instruction.op()
            if self.pause:
                self.pause = False
                return self.memory
        return self.memory

            
    def post(self):
        print("Power on self test .", end='')
        sys.stdout.flush()
        for test in test_vectors:
            self.reset()
            debug("\n----- RESET -----\n")
            if 'name' in test:
                debug(f"Running test {test['name']}")
            if 'input' in test:
                self.data_in = test['input']
            got = self.memory = test['in']
            debug(f"Test input: {got}")
            while self.running:
                self.go()
            
            if 'out' in test and test['out'] != got:
                want = test['out']
                print(f"\nWant {want}\nGot  {got}\n")
                sys.exit(1)
            if 'output' in test and test['output'] != self.data_out:
                want = test['output']
                got  = self.data_out
                print(f"\nWanted out {want}\nGot        {got}\n")
                sys.exit(2)
            print(".", end='')
            sys.stdout.flush()
        def calculate(noun, verb):
            self.reset()
            mem = program.copy()
            # Apply patches
            mem[1] = noun
            mem[2] = verb
            result = self.run(mem)
            return(result[0])
        
        assert calculate(12,  2) == 3101844
        print(".", end='')
        sys.stdout.flush()
        assert calculate(84, 78) == 19690720
        print(".", end='')
        sys.stdout.flush()
        self.reset()
        print(" done")


if __name__ == "__main__":
    cpu = IntcodeCPU()
    cpu.post()
