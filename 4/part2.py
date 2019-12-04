def check_adjacent_digits(input):
    i = list(str(input))
    return i[0] == i[1] or i[1] == i[2] or i[2] == i[3] or i[3] == i[4] or i[4] == i[5]


def check_left_to_right(input):
    prev = int(-1)
    for i in list(str(input)):
        if int(i) < prev:
            return False
        prev = int(i)
    return True


def check_group(input):
    x = list(str(input))
    prev = None
    cur = []
    groups = []
    for i in x:
        if i is not prev:
            groups.append(cur)
            cur = []
        cur.append(i)
        prev = i
    groups.append(cur)
    groups = groups[1:]
    uniq = list(map(lambda x: len(x), groups))
    return 2 in uniq


def check_number(input):
    adjacent = check_adjacent_digits(input)
    ltr = check_left_to_right(input)
    group = check_group(input)
    return adjacent and ltr and group


# assert check_number(111111) == True
assert check_number(111111) == False
assert check_number(223450) == False
assert check_number(123789) == False
assert check_number(112233) == True
assert check_number(123444) == False
assert check_number(111122) == True

found = []
for num in range(256310, 732736):
    if check_number(num):
        # print(f"found: {num}")
        found.append(num)

print(len(found))
