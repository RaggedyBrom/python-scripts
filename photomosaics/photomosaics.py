from os import listdir, path
from math import sqrt
from random import randint
from statistics import mean
from datetime import datetime
import json

from PIL import Image, ImageDraw

# Mosaic settings and input
input_filepath = input('Enter the path to the input image: ')
input_filename = path.splitext(path.split(input_filepath)[1])[0]
source_directory = input('Enter the path to the source images directory: ')
sq_size = input('Enter the size of each square in pixels or press ENTER ' +
                'for the default value of 100: ')
if sq_size:
    sq_size = int(sq_size)
else:
    sq_size = 100

max_output_size = input('Enter the max width/height of the output ' +
                          'in pixels, or press ENTER for the default ' +
                          'value of 10800: ')
if max_output_size:
    max_output_size = int(max_output_size)
else:
    max_output_size = 10800

# Image initialization
input_image = Image.open(input_filepath)

if input_image.width > input_image.height:
    output_width = max_output_size
    output_height = int((input_image.height * output_width) / input_image.width)
else:
    output_height = max_output_size
    output_width = int((input_image.width * output_height) / input_image.height)

f = open('rgb_cache.json', 'r')
cache = json.load(f)
f.close()

# Iterate over each square of an image and calculate the average
# RGB value of the square, then draw a square of that size and RGB
# value to a new image.
def construct_pixellated_mosaic():
    pixellated = Image.new('RGB', (input_image.width, input_image.height),
                           color=(255, 255, 255))
    pixel_draw = ImageDraw.Draw(pixellated)
    width, height = input_image.size
    for sq_y in range(0, height, sq_size):
        for sq_x in range(0, width, sq_size):
            square_RGB = square_average_RGB(sq_y, sq_x)
            draw_pixellated_square(sq_x, sq_y, square_RGB, pixel_draw)
    pixellated.save(input_filename + '_pixellated_' + str(sq_size) + '.jpg',
                    quality=100)
    print('Done.')

# Iterate over each square of an image, calculate the
# average RGB value of the square, match that average RGB to an image
# from the source directory, and then paste that image at the square's
# location onto a new output image. The result is a photomosaic.
def construct_output_mosaic():
    output_image = Image.new('RGB', (output_width, output_height),
                             color=(255, 255, 255))
    width, height = input_image.size
    for sq_y in range(0, height, sq_size):
        for sq_x in range(0, width, sq_size):
            print('Checking the square in column ' + str(int(sq_x / sq_size)) +
                  ', row ' + str(int(sq_y / sq_size)))
            square_RGB = square_average_RGB(sq_y, sq_x)
            source = match_by_color_difference(square_RGB)
            print('Found the nearest matching source image.\n')
            draw_output_square(sq_x, sq_y, output_image, source)
    output_image.save(input_filename + '_output_' + str(sq_size) + '.jpg',
                      quality=100)
    print('Done.')

# Paste the given source image to the specified coordinates on the outpute image.
def draw_output_square(sq_x, sq_y, output_image, source_image):
    resized_width = int((output_width * sq_size) / input_image.width)
    resized_height = int((output_height * sq_size) / input_image.height)
    source = source_image.resize((resized_width, resized_height))
    source_x_value = int((sq_x * resized_width) / sq_size)
    source_y_value = int((sq_y * resized_height) / sq_size)
    output_image.paste(source, (source_x_value, source_y_value))
            
# Draws a square of the given RGB value to the pixellated output image.
def draw_pixellated_square(sq_x, sq_y, square_RGB, pixel_draw):
    R, G, B = square_RGB
    pixel_draw.rectangle([(sq_x, sq_y),(sq_x+sq_size,sq_y+sq_size)],
                   fill=(R, G, B))

# Find the average RGB value of a specified square on the input image.
def square_average_RGB(sq_y, sq_x):
    total_R = 0
    total_G = 0
    total_B = 0
    pixel_number = 0
    for y in range(sq_size):
        for x in range(sq_size):
            try:
                R, G, B = input_image.getpixel((x+sq_x, y+sq_y))
            except IndexError:
                continue               
            total_R += R
            total_G += G
            total_B += B
            pixel_number += 1
    average_R = round(total_R / pixel_number)
    average_G = round(total_G / pixel_number)
    average_B = round(total_B / pixel_number)
    return (average_R, average_G, average_B)

# Finds the average RGB value of a source image by iterating over each pixel.
# Deprecated by "source_average_RGB_by_lists".
def average_RGB(source_image):
    width, height = source_image.size
    total_R = 0
    total_G = 0
    total_B = 0
    pixel_number = 0
    for y in range(height):
        for x in range(width):
            R, G, B = source_image.getpixel((x, y))
            total_R += R
            total_G += G
            total_B += B
            pixel_number += 1
    average_R = round(total_R / pixel_number)
    average_G = round(total_G / pixel_number)
    average_B = round(total_B / pixel_number)
    return (average_R, average_G, average_B)

# Finds the average RGB value of a source image by finding
# the mean value of each color band in the image.
# Deprecated by "source_average_RGB_by_lists".
def average_RGB_by_band(image):
    average_color = [mean(image.getdata(band)) for band in range(3)]
    return average_color

# Find the average RGB value of a source image by using
# list comprehensions to count the number of pixels of each color in the image,
# multiplying the count by each color to get the total representation of that
# color, and then dividing the amount of color by the number of pixels.
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

# Finds the color difference (by means of the Pythagorean
# theorem in three dimensions) of the average square RGB and all of the
# source image average RGBs.  The function returns the source image with
# the lowest color difference.
def match_by_color_difference(square_RGB):
    sqR, sqG, sqB = square_RGB
    best_color_difference = 999999
    best_source_images = []
    for filename in listdir(source_directory):
        if filename in cache:
            source_average_RGB = cache[filename]                   
        else:
            print('Checking source file ' + filename)
            source_image = Image.open(source_directory + '//' + filename)
            source_average_RGB = source_average_RGB_by_lists(source_image)
            print('The source file\'s RGB value is ' + str(source_average_RGB))
            print('Adding the RGB value to the cache...')
            cache[filename] = source_average_RGB
        srcR, srcG, srcB = source_average_RGB
        color_difference = sqrt((srcR - sqR)**2 + (srcG - sqG)**2 +
                                (srcB - sqB)**2)
        if color_difference < best_color_difference:
            best_color_difference = color_difference
            source_image = Image.open(source_directory + '//' + filename)
            best_source_images = []
            best_source_images.append(source_image)
        elif color_difference == best_color_difference:
            source_image = Image.open(source_directory + '//' + filename)
            best_source_images.append(source_image)
        else:
            continue
        
    return best_source_images[randint(0, len(best_source_images) - 1)]


construct_output_mosaic()
input()
