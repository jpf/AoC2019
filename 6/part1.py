import pprint

def load_orbits(filename):
    orbits = {}
    orbiting = {}
    with open(filename) as f:
        for line in f.readlines():
            line = line.rstrip()
            a, b = line.split(')')
            if a not in orbiting:
                orbiting[a] = []
            orbiting[a].append(b)
            orbits[b] = a
    print("Orbits:")
    pprint.pprint(orbits)
    print("Orbiting:")
    pprint.pprint(orbiting)
    return orbits

def count_orbits_for(planet, orbits, count=0):
    if planet not in orbits:
        print(f"{planet} has no orbits")
        return(count)
    parent= orbits[planet]
    print(f"{planet} orbits {parent}")
    count += 1
    return count_orbits_for(parent, orbits, count)

def count_total_orbits(orbits):
    total = 0
    for planet, value in orbits.items():
        count = count_orbits_for(planet, orbits)
        print(f"{planet} has {count} orbits")
        total += count
    return total

tests = [
    {'input': load_orbits('orbit_map_test.txt'),
     'output': 42},
    ]

for test in tests:
    orbits = test['input']
    want = test['output']
    got  = count_total_orbits(orbits)

    print(f"w: {want}\ng: {got}")


puzzle_input = load_orbits('orbit_map_puzzle_input.txt')
total = count_total_orbits(puzzle_input)
print(total)
