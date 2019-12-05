# Intcode CPU

# TEST program
program = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,11,91,225,1002,121,77,224,101,-6314,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1102,74,62,225,1102,82,7,224,1001,224,-574,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1101,28,67,225,1102,42,15,225,2,196,96,224,101,-4446,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1101,86,57,225,1,148,69,224,1001,224,-77,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1101,82,83,225,101,87,14,224,1001,224,-178,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,38,35,225,102,31,65,224,1001,224,-868,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1101,57,27,224,1001,224,-84,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1101,61,78,225,1001,40,27,224,101,-89,224,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,226,224,1002,223,2,223,1006,224,329,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,344,101,1,223,223,1107,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,1007,226,226,224,102,2,223,223,1006,224,374,101,1,223,223,7,677,677,224,102,2,223,223,1005,224,389,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,404,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,419,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,434,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,464,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,479,101,1,223,223,1007,226,677,224,1002,223,2,223,1006,224,494,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,524,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,539,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,554,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,569,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,677,224,102,2,223,223,1005,224,599,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,614,101,1,223,223,8,226,226,224,102,2,223,223,1006,224,629,101,1,223,223,108,226,677,224,102,2,223,223,1005,224,644,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,659,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226]

def load(memory, index, mode, values):
    print(f"index: {index} mode: {mode} values: {values}")
    output = []
    for x in range(1, values):
        print(f"x: {x}")
        if mode[x] == "1": # Immediate
            output.append(memory[index + x])
        elif mode[x] == "0": # Position
            position = memory[index + x]
            output.append(memory[position])
        else:
            part("Load Error")
    output.append(values) # Offset to use
    return output

inputs = []

def run(memory):
    running = True
    index = 0
    mode = []
    while(running):
        opcode = memory[index]
        offset = 0
        
        abcde = str(opcode)
        while len(abcde) < 5:
            abcde = "0" + abcde
        opcode = int(abcde[3:5])
        mode = list(abcde[0:3])
        mode.reverse()
        mode.insert(0, None) # Always skip self
        
        if opcode == 99:
            break

        if opcode == 1:   # Add
            a, b, target, offset = load(memory, index, mode, 4)
            memory[target] = a + b
        elif opcode == 2: # Multiply
            a, b, target, offset = load(memory, index, mode, 4)
            memory[target] = a * b
        elif opcode == 3:  # Save to address
            target, offset = load(memory, index, mode, 1)
            memory[target] = inputs.pop(0)
        elif opcode == 4:  # Output address
            target, offset = load(memory, index, mode, 1)
            print(memory[target])
            offset = 2
        else:
            print("Parse error!")
        if offset == 0:
            print("Offset error")
        index = index + offset
    return memory

test_vectors = [
    {'in': [1,0,0,0,99],          'out': [2,0,0,0,99]},
    {'in': [2,3,0,3,99],          'out': [2,3,0,6,99]},
    {'in': [2,4,4,5,99,0],        'out': [2,4,4,5,99,9801]},
    {'in': [1,1,1,4,99,5,6,0,99], 'out': [30,1,1,4,2,5,6,0,99]},
]

for vector in test_vectors:
    want = vector['out']
    got = run(vector['in'])
    print(f"Want {want}\nGot  {got}\n")
    # assert want == got

def calculate(noun, verb):
    mem = program.copy()
    # Apply patches
    mem[1] = noun
    mem[2] = verb
    result = run(mem)
    return(result[0])

assert calculate(12, 2) == 3101844

# inputs.append(1)
# run(program)
