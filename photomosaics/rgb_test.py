from statistics import mean

from PIL import Image, ImageDraw

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

def average_RGB_by_band(image):
    average_color = [mean(image.getdata(band)) for band in range(3)]
    return average_color

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

image_path = input('Please enter the path to the image to calculate the RGB ' +
              'values of: ')
image = Image.open(image_path)

print('The average RGB by pixel count is ' + str(average_RGB(image)))
print('The average RGB by color band is ' + str(average_RGB_by_band(image)))
print('The average RGB by list comprehensions is ' + str(average_RGB_by_lists(image)))
input('Press any key to exit.')
