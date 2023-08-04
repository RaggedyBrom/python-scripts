from os import listdir
import json

from PIL import Image

def average_RGB_by_lists(image):
    """
    Given PIL Image, return average value of color as (r, g, b)
    """
    # no. of pixels in image
    npixels = image.size[0]*image.size[1]
    # get colors as [(cnt1, (r1, g1, b1)), ...]
    cols = image.getcolors(npixels)
    # get [(c1*r1, c1*g1, c1*b1),...]
    sumRGB = [(x[0]*x[1][0], x[0]*x[1][1], x[0]*x[1][2]) for x in cols] 
    # calculate (sum(ci*ri)/np, sum(ci*gi)/np, sum(ci*bi)/np)
    # the zip gives us [(c1*r1, c2*r2, ..), (c1*g1, c1*g2,...)...]
    avg = tuple([round(sum(x)/npixels) for x in zip(*sumRGB)])
    return avg

source_directory = input('Please enter the path to the source directory: ')
cache = {}

f = open('rgb_cache.json', 'w')

files_processed = 0

for filename in listdir(source_directory):
    if filename not in cache:
        source_image = Image.open(source_directory + '//' + filename)
        average_RGB = average_RGB_by_lists(source_image)
        cache[filename] = average_RGB
        files_processed += 1
    else:
        continue
    
json.dump(cache, f)
f.close()
print('Done.')
print(str(files_processed) + ' values successfully cached.')
print('The length of the cache is ' + str(len(cache)))
input()
