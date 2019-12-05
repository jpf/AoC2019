# Intcode CPU
import sys
import os

program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,5,19,23,2,9,23,27,1,6,27,31,1,31,9,35,2,35,10,39,1,5,39,43,2,43,9,47,1,5,47,51,1,51,5,55,1,55,9,59,2,59,13,63,1,63,9,67,1,9,67,71,2,71,10,75,1,75,6,79,2,10,79,83,1,5,83,87,2,87,10,91,1,91,5,95,1,6,95,99,2,99,13,103,1,103,6,107,1,107,5,111,2,6,111,115,1,115,13,119,1,119,2,123,1,5,123,0,99,2,0,14,0]

TEST = [   3, 225,
      #    0    1
           1, 225,  6,    6,
      #    2    3   4     5
        1100,   1, 238, 225,
      #    6    7    8    9
         104,   0,
      #   10   11
        1101,  11,  91, 225,
        1002, 121,  77, 224,
        101,-6314,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1102,74,62,225,1102,82,7,224,1001,224,-574,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1101,28,67,225,1102,42,15,225,2,196,96,224,101,-4446,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1101,86,57,225,1,148,69,224,1001,224,-77,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1101,82,83,225,101,87,14,224,1001,224,-178,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,38,35,225,102,31,65,224,1001,224,-868,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1101,57,27,224,1001,224,-84,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1101,61,78,225,1001,40,27,224,101,-89,224,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,226,224,1002,223,2,223,1006,224,329,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,344,101,1,223,223,1107,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,1007,226,226,224,102,2,223,223,1006,224,374,101,1,223,223,7,677,677,224,102,2,223,223,1005,224,389,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,404,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,419,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,434,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,464,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,479,101,1,223,223,1007,226,677,224,1002,223,2,223,1006,224,494,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,524,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,539,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,554,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,569,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,677,224,102,2,223,223,1005,224,599,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,614,101,1,223,223,8,226,226,224,102,2,223,223,1006,224,629,101,1,223,223,108,226,677,224,102,2,223,223,1005,224,644,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,659,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226]

POSITION_MODE = "0"
IMMEDIATE_MODE = "1"

DEBUG = os.getenv('DEBUG', False)

def debug(msg):
    if DEBUG:
        print(msg)

class IntcodeCPU:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.instruction_pointer = 0
        self.show_output = False
        self.memory = []
        self.data_in = []
        self.output = []

    def load_params(self, num=3, mode=[]):
        width = num + 1
        output = []

        # "Parameters that an instruction writes to will never be in immediate mode."
        # (read/write/jump)
        # This code caused me several hours of heartache!!!
        if num > 2:
            mode[width - 1] = IMMEDIATE_MODE
        debug(f"load_params ip: {self.instruction_pointer}")
        start = self.instruction_pointer
        end = self.instruction_pointer + width
        debug(f"load_params input: {self.memory[start:end]}")
        debug(f"load_params mode:  {mode}")
        for arg in range(1, width):
            if mode[arg] == IMMEDIATE_MODE:
                output.append(self.memory[self.instruction_pointer + arg])
            elif mode[arg] == POSITION_MODE:
                position = self.memory[self.instruction_pointer + arg]
                output.append(self.memory[position])
            else:
                print("Unable to determine mode")
                sys.exit(100)

        # output.append(self.memory[self.instruction_pointer + width]) # target

        self.offset = width
        debug(f"params: {output}")
        if len(output) == 1:
            return(output[0])
        else:
            return(output)

    def load_opcode(self):
        raw_opcode = self.memory[self.instruction_pointer]
        abcde = str(raw_opcode)
        while(len(abcde) < 5):
            abcde = "0" + abcde
        opcode = int(abcde[3:])
        mode = [
            None, # No mode needed for the opcode
            abcde[2],
            abcde[1],
            abcde[0],
        ]
        return opcode, mode

    def dump_memory(self):
        if not DEBUG:
            return
        print("memory:")
        for address, value in enumerate(self.memory):
            ptr = " "
            if address == self.instruction_pointer:
                ptr = ">"
            print(f"{ptr}{address: >5}: {value: >5}")
        print("")
        
    
    def run(self, memory):
        self.memory = memory
        debug("Loaded memory")
        self.dump_memory()
        running = True
        while(running):
            opcode, mode = self.load_opcode()

            if opcode == 99:
                break
            debug(f"ip: {self.instruction_pointer}\t raw opcode: {self.memory[self.instruction_pointer]}\t mode {mode}")
            self.dump_memory()
            if opcode == 1:   # Add
                a, b, target = self.load_params(mode=mode)
                self.memory[target] = a + b
                debug(f"ADD: {a} + {b} set {target} to {self.memory[target]}")
                self.instruction_pointer += self.offset
            elif opcode == 2: # Multiply
                a, b, target = self.load_params(mode=mode)
                self.memory[target] = a * b
                self.instruction_pointer += self.offset
            elif opcode == 3: # Input
                mode[1] = IMMEDIATE_MODE
                target = self.load_params(num=1, mode=mode)
                val = self.data_in.pop(0)
                self.memory[target] = val
                debug(f"stored {val} at {target}")
                self.instruction_pointer += self.offset
            elif opcode == 4: # Output
                val = self.load_params(num=1, mode=mode)
                output = val
                self.output.append(output)
                if self.show_output:
                    print(output)
                    debug(f"output: {output}")
                self.instruction_pointer += self.offset
            elif opcode == 5: # jump-if-true
                check, jump_to = self.load_params(num=2, mode=mode)
                debug(f"{check} != 0 (jnz)")
                loc = self.instruction_pointer + self.offset
                if check != 0:
                    loc = jump_to
                debug(f"... ip set to {loc}")
                self.instruction_pointer = loc
            elif opcode == 6: # jump-if-false
                check, jump_to = self.load_params(num=2, mode=mode)
                debug(f"{check} == 0 (jz)")
                loc = self.instruction_pointer + self.offset
                if check == 0:
                    loc = jump_to
                debug(f"... ip set to {loc}")
                self.instruction_pointer = loc
            elif opcode == 7: # less than
                a, b, target = self.load_params(num=3, mode=mode)
                value = 0
                if a < b:
                    value = 1
                debug(f"{a} < {b} writing {value} to {target}")
                self.memory[target] = value
                self.instruction_pointer += self.offset
            elif opcode == 8: # equals
                a, b, target = self.load_params(num=3, mode=mode)
                value = 0
                if a == b:
                    value = 1
                debug(f"{a} == {b} writing {value} to {target}")
                self.memory[target] = value
                self.instruction_pointer += self.offset
            else:
                print("Parse error!")
                sys.exit(101)
        return self.memory


larger_example = [   3, 21,
                 #   0   1
                  1008, 21,  8, 20,
                 #   2   3   4   5
                  1005, 20, 22,
                 #   6   7   8  
                   107,  8, 21, 20,
                 #   9  10  11  12
                  1006, 20, 31,
                 #  13  14  15
                  1106,  0, 36,
                 #  16  17  18
                  98,    0,  0,
                 #  19  20  21
                  1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

position_mode_eq_eight = [3,9,8,9,10,9,4,9,99,-1,8]
position_mode_lt_eight = [3,9,7,9,10,9,4,9,99,-1,8]

position_mode_jmp_test = [ 3, 12,
                         # 0   1
                           6, 12, 15,
                         # 2   3   4
                           1, 13, 14, 13,
                         # 5   6   7   8
                           4, 13,
                         # 9  10
                          99, -1, 0, 1, 9
                         #11  12 13 14 15
]
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

    {'in':     [3,4,99,0,0],
     'out':    [3,4,99,0,42],
     'input':  [42]},
    {'in':     [4,4,99,0,42],
     'out':    [4,4,99,0,42],
     'output': [42]},
    {'in':     [3,0,4,0,99],
     'out':    [42,0,4,0,99],
     'input':  [42],
     'output': [42]},
    {'in':     [1002,4,3,4,33],
     'out':    [1002,4,3,4,99]},

    {'in':     larger_example,
     'input':  [8],
     'output': [1000],
    },
    {'in':     larger_example,
     'input':  [7],
     'output': [999],
    },
    {'in':     larger_example,
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

    
    {'in': immediate_mode_eq_eight, 'input':  [7], 'output': [0] },
    {'in': immediate_mode_eq_eight, 'input':  [8], 'output': [1] },
    {'in': immediate_mode_eq_eight, 'input':  [9], 'output': [0] },

    {'in': immediate_mode_lt_eight, 'input':  [7], 'output': [1] },
    {'in': immediate_mode_lt_eight, 'input':  [8], 'output': [0] },

    {'in': list(immediate_mode_jmp_test), 'input':  [0], 'output': [0] },
    {'in': list(immediate_mode_jmp_test), 'input':  [-1], 'output': [1] },
    {'in': list(immediate_mode_jmp_test), 'input':  [1], 'output': [1] },
]

cpu = IntcodeCPU()

print("Power on self test .", end='')
sys.stdout.flush()
for vector in test_vectors:
    cpu.reset()
    debug("\n----- RESET -----\n")
    if 'name' in vector:
        debug(f"Running test {vector['name']}")
    cpu.dump_memory()
    if 'input' in vector:
        cpu.data_in = vector['input']
    got = cpu.run(vector['in'])
    
    if 'out' in vector and vector['out'] != got:
        want = vector['out']
        print(f"\nWant {want}\nGot  {got}\n")
        sys.exit(1)
    if 'output' in vector and vector['output'] != cpu.output:
        want = vector['output']
        got  = cpu.output
        print(f"\nWanted out {want}\nGot        {got}\n")
        sys.exit(2)
    print(".", end='')
    sys.stdout.flush()

def calculate(noun, verb):
    cpu.reset()
    mem = program.copy()
    # Apply patches
    mem[1] = noun
    mem[2] = verb
    result = cpu.run(mem)
    return(result[0])

assert calculate(12, 2) == 3101844

assert calculate(84, 78) == 19690720

print(" done")

cpu.reset()
cpu.data_in = [5]
cpu.show_output = True
cpu.run(TEST)

# for try_noun in range(0, 100):
#     for try_verb in range(0, 100):
#         answer = 100 * try_noun + try_verb
#         result = calculate(try_noun, try_verb)
#         if result == 19690720:
#             print(f"noun: {try_noun} verb: {try_verb}")
#             print(answer)
