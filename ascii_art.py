from PIL import Image
from colorama import init, Fore
init(autoreset=True)

# Settings
filename = ''       # Set to name of image file
inverted = False
color = False
b_setting = 'luminosity'

# Basic initialization
im = Image.open(filename)

# Resize the image if it is larger than 300x300
max_size = 250
if im.width > max_size or im.height > max_size:
    if im.width > im.height:
        factor = max_size / im.width
    else:
        factor = max_size / im.height
    im = im.resize((int(im.width * factor), int(im.height * factor)))   

# Construct the pixel matrix from each pixel's RGB values
pixel_matrix = []
for x in range(im.width):
    column = []
    for y in range(im.height):
        column.append(im.getpixel((x,y)))
    pixel_matrix.append(column)

# Define the brightness mappings
def b_mapping(R, G, B, b_setting):
    if b_setting == 'average':
        return round((R + G + B) / 3)
    elif b_setting == 'min_max':
        return round((max(R, G, B) + min(R, G, B)) / 2)
    elif b_setting == 'luminosity':
        return round(0.21 * R + 0.72 * G + 0.07 * B)

def b_inversion(b):
    return 255 - b

# Construct the brightness matrix from the pixel matrix
b_matrix = []
for x in pixel_matrix:
    column = []
    for y in x:
        R, G, B = y
        brightness = b_mapping(R, G, B, b_setting)
        if inverted:
            brightness = b_inversion(brightness)
            column.append((R, G, B, brightness))
        else:
            column.append((R, G, B, brightness))
    b_matrix.append(column)
        
# Construct the character set dictionary
characters = ('`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCL' +
              'Q0OZmwqpdbkhao*#MW&8%B@$')
character_set = {}
for index, character in enumerate(characters):
        character_set[index * 4] = character

# Construct the ASCII matrix from the brightness matrix
ascii_matrix = []
for x in b_matrix:
    column = []
    for y in x:
        R, G, B, b = y
        value = (round(b / 4) * 4)
        column.append((R, G, B, character_set[value]))
    ascii_matrix.append(column)

# Define color mapping
def color_mapping(R, G, B):
    if R > 180 and G < 50 and B < 50:
        return Fore.RED
    elif G > 180 and R < 50 and B < 50:
        return Fore.GREEN
    elif B > 180 and R < 50 and G < 50:
        return Fore.BLUE
    elif R > 180 and G > 180 and B < 50:
        return Fore.YELLOW
    elif R > 180 and B > 180 and G < 50:
        return Fore.MAGENTA
    elif G > 180 and B > 180 and R < 50:
        return Fore.CYAN
    else:
        return ''

# Print the ASCII matrix
for y in range(len(ascii_matrix[0])):
    for x in range(len(ascii_matrix)):
        R, G, B, c = ascii_matrix[x][y]
        if color:
            print(color_mapping(R, G, B) + (c * 3), end='')
        else:
            print((c * 3), end='')
    print()

k = input()
