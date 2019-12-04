def check_adjacent_digits(input):
    i = list(str(input))
    return i[0] == i[1] or i[1] == i[2] or i[2] == i[3] or i[3] == i[4] or i[4] == i[5]


def check_left_to_right(input):
    prev = int(-1)
    for i in list(str(input)):
        # print(f"{i} < {prev}")
        if int(i) < prev:
            return False
        prev = int(i)
    return True


def check_number(input):
    adjacent = check_adjacent_digits(input)
    ltr = check_left_to_right(input)
    return adjacent and ltr


assert check_number(111111) == True
assert check_number(223450) == False
assert check_number(123789) == False

found = []
for num in range(256310, 732736):
    if check_number(num):
        found.append(num)

print(len(found))
