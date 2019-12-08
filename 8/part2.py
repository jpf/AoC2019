# 25 pixels wide and 6 pixels tall.

from PIL import Image

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

def resolve(l, x, y, layers):
    pix = layers[l][x][y]
    if pix != "2":
        return(pix)
    lower = l - 1
    if lower <= 0:
        pix = "4"
    return(resolve(lower, x, y, layers))

layers = list(reversed(layers))
for l, layer in enumerate(layers):
    img = []
    for x, line in enumerate(layer):
        out_line = []
        for y, pix in enumerate(line):
            out = ""
            if pix == "2":
                pix = resolve(l, x, y, layers)

            if pix == "0":
                out = 0
            elif pix == "1":
                out = 1
            elif pix == "4":
                out = "_"
            else:
                out = "."
            out_line.append(out)
        img.append(out_line)

pic = Image.new("1", (max_width, max_height), color=1)
for x, line in enumerate(img):
    for y, pix in enumerate(line):
        pic.putpixel((y, x), pix)
pic.show()
