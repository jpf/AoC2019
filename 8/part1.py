# 25 pixels wide and 6 pixels tall.

input = ""
with open('img') as f:
    for line in f.readlines():
        input += line


def count_of(integer, layer):
    my = sum(layer, [])
    count = {}
    for x in my:
        if x not in count:
            count[x] = 0
        count[x] += 1
    return(count[integer])

layers = []
layer = []
line = []
max_width = 25
max_height = 6
for pixel in list(input):
    line.append(pixel)
    if len(line) >= max_width:
        layer.append(list(line))
        line = []
    if len(layer) >= max_height:
        layers.append(list(layer))
        layer = []

zeros = []

# print(layers[0])
# print(layers[-1])
for layer in layers:
    zeros.append(count_of('0', layer))
# sz = sorted(zeros)
# print(f"zeros count: {sz}")
idx = zeros.index(min(zeros))
x = layers[idx]

y = sum(x, [])
y = sorted(y)
# print(y)

ones = count_of('1', x)
twos = count_of('2', x)

# print(f"{ones} * {twos}")

print(int(ones) * int(twos))
