# Intcode CPU

program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,5,19,23,2,9,23,27,1,6,27,31,1,31,9,35,2,35,10,39,1,5,39,43,2,43,9,47,1,5,47,51,1,51,5,55,1,55,9,59,2,59,13,63,1,63,9,67,1,9,67,71,2,71,10,75,1,75,6,79,2,10,79,83,1,5,83,87,2,87,10,91,1,91,5,95,1,6,95,99,2,99,13,103,1,103,6,107,1,107,5,111,2,6,111,115,1,115,13,119,1,119,2,123,1,5,123,0,99,2,0,14,0]

def run(memory):
    running = True
    index = 0
    while(running):
        opcode = memory[index]
        
        if opcode == 99:
            break
        
        a      = memory[index + 1]
        b      = memory[index + 2]
        target = memory[index + 3]

        if opcode == 1:   # Add
            memory[target] = memory[a] + memory[b]
        elif opcode == 2: # Multiply
            memory[target] = memory[a] * memory[b]
        else:
            print("Parse error!")
        index = index + 4
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
    assert want == got
    # print(f"Want {want}\nGot  {got}\n")

def calculate(noun, verb):
    mem = program.copy()
    # Apply patches
    mem[1] = noun
    mem[2] = verb
    result = run(mem)
    return(result[0])

assert calculate(12, 2) == 3101844

for try_noun in range(0, 100):
    for try_verb in range(0, 100):
        answer = 100 * try_noun + try_verb
        result = calculate(try_noun, try_verb)
        if result == 19690720:
            print(answer)
