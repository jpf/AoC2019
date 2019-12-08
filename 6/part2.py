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
    return orbits

def shortest_path(planet, orbits, path=None, target=None):
    # The == test here is key, 'is' is not the same is '=='
    if target and planet == target:
        return(path)
    if not path:
        path = []
    if planet not in orbits:
        return(path)
    parent = orbits[planet]
    path.append(parent)
    return shortest_path(parent, orbits, path=path, target=target)
    

def count_orbits_for(planet, orbits, count=None, target=None):
    path = shortest_path(planet, orbits, target=target)
    length = len(path) - 1
    return length


def count_total_orbits(orbits):
    total = 0
    for planet, value in orbits.items():
        count = count_orbits_for(planet, orbits)
        # print(f"{planet} has {count} orbits")
        total += count
    return total

def path_from(planet, orbits, path=None):
    if not path:
        path = {}
    if planet not in orbits:
        return(path)
    parent = orbits[planet]
    path[planet] = parent
    return path_from(parent, orbits, path)


def find_common_planet(orbits):
    common = []
    for planet in orbits.keys():
        if len(orbits[planet]) > 1:
            common.append(planet)
    if len(common):
        return common[0]
    return None


def minimum_orbits_between(source, dest, orbits):
    path_a = path_from(source, orbits)
    path_b = path_from(dest, orbits)

    optimized = {}
    for planet, parent in path_a.items():
        if parent not in optimized:
            optimized[parent] = []
        optimized[parent].append(planet)
    for planet, parent in path_b.items():
        if parent not in optimized:
            optimized[parent] = []
        if planet not in optimized[parent]:
            optimized[parent].append(planet)

    common_planet = find_common_planet(optimized)
    
    oorbits = orbits.copy()
    # oorbits = optimized.copy()
    short_a = shortest_path(source, oorbits, target=common_planet)[:-1]
    short_b = shortest_path(dest, oorbits, target=common_planet)

    short_b.reverse()
    short = short_a + short_b
    return short
    # 494 is too high

def make_dot(orbits, special):

    print("digraph Orbits {")
    print("\tnode [color = white, style = filled];")
    for planet in special:
        print(f'\t"{planet}" [color=red]')
    for planet, parent in orbits.items():
        print(f'\t"{planet}" -> "{parent}";')
    print("}")
        
test_input = load_orbits('orbit_map_puzzle_input.txt')
tests = [
    {'input': load_orbits('orbit_map_test.txt'),
     'output': 42},
    {'input': test_input.copy(),
     'output': 344238},
    ]

orbit_map = load_orbits('orbit_map_part2.txt')
found = minimum_orbits_between('YOU', 'SAN', orbit_map)
want = 4
got = len(found) - 1
assert want == got
# print(f"w: {want}\ng: {got}")
# make_dot(orbit_map, special=found)

orbit_map = load_orbits('orbit_map_puzzle_input.txt')
found = minimum_orbits_between('YOU', 'SAN', orbit_map)
# make_dot(orbit_map, special=found)
# want = '?'
got = len(found) - 1
print(got)
