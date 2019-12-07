import sys
from cpu import IntcodeCPU

tests = [{'phase_settings': [4,3,2,1,0],
          'program': [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
          'output': 43210},
         {'phase_settings': [0,1,2,3,4],
          'program': [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],
          'output': 54321},
         {'phase_settings': [1,0,4,3,2],
          'program': [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0],
          'output': 65210},
         ]


cpu = IntcodeCPU()
cpu.post()

def are_running(amps):
    statuses = []
    for amp in amps:
        statuses.append(amp.running)
    # print(f"are running: {statuses}")
    statuses = set(statuses)
    # print(f"are running: {statuses}")
    if len(statuses) == 1:
        return list(statuses)[0]
    else:
        return True

def run_amp(phase_settings, program):
    amps = [IntcodeCPU(),IntcodeCPU(),IntcodeCPU(),IntcodeCPU(),IntcodeCPU()]
    for cpu_num in [0, 1, 2, 3, 4]:
        amp = amps[cpu_num]
        amp.memory = list(program)
        amp.data_in.append(phase_settings[cpu_num])
    
    last_output = 0
    while are_running(amps):
        for amp in amps:
            # if not amp.running:
            #     print("STOPPED")
            #     print(amp)
            #     continue
            amp.data_in.append(last_output)
            amp.go()
            # print(f"OUTPUT: {amp.output}")
            last_output = amp.output[-1]
    return last_output
    

for test in tests:
    # print(test)
    want = test['output']
    # print(f"want: {want}")
    got = run_amp(test['phase_settings'], test['program'])
    # print(f"got:  {got}")
    assert want == got

amp_program = [3,8,1001,8,10,8,105,1,0,0,21,42,51,60,77,94,175,256,337,418,99999,3,9,1001,9,4,9,102,5,9,9,1001,9,3,9,102,5,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,1001,9,3,9,4,9,99,3,9,101,4,9,9,1002,9,4,9,101,5,9,9,4,9,99,3,9,1002,9,5,9,101,3,9,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99]
    
import itertools

answers = []
for permutation in itertools.permutations([0, 1, 2, 3, 4]):
    answers.append(run_amp(permutation, amp_program))

assert max(answers) == 18812

tests2 = [
    {'phase_settings': [4,3,2,1,0],
     'program': [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
     'output': 43210},
    {'phase_settings': [0,1,2,3,4],
     'program': [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],
     'output': 54321},
    {'phase_settings': [1,0,4,3,2],
     'program': [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0],
     'output': 65210},
    {'phase_settings': [9,8,7,6,5],
     'program': [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],
     'output': 139629729},
    {'phase_settings': [9,7,8,5,6],
     'program': [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10],
     'output': 18216},
]

print("running tests ...",end="")
sys.stdout.flush()

for test in tests2:
    want = test['output']
    # print(f"want: {want}")
    got = run_amp(test['phase_settings'], test['program'])
    # print(f"got:  {got}")
    # sys.stdout.flush()
    assert want == got
print("done")

answers = []
for permutation in itertools.permutations([5, 6, 7, 8, 9]):
    answers.append(run_amp(permutation, amp_program))

print(answers)
print(max(answers))

