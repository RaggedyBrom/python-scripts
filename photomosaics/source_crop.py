from os import walk, path
import uuid
from PIL import Image

input_directory = input('Please enter the path to the input directory: ')
output_directory = input('Please enter the path to the output directory: ')

def source_crop(directory):
    file_count = 0
    open_error_count = 0
    crop_error_count = 0
    crop_count = 0
    for folder, subfolders, filenames in walk(directory):
        print('Scanning folder: ' + folder)
        for filename in filenames:
            file_count += 1
            try:
                im = Image.open(path.abspath(folder) + '//' + filename)
            except:
                print('There was an error opening ' + filename)
                open_error_count += 1
                continue
            width, height = im.size
            if width > height:
                x1 = (width - height) / 2
                y1 = 0
                x2 = x1 + height
                y2 = height
            elif height > width:
                x1 = 0
                y1 = (height - width) / 2
                x2 = width
                y2 = y1 + width
            else:
                x1 = 0
                y1 = 0
                x2 = width
                y2 = height
            try:
                cropped = im.crop((x1, y1, x2, y2))
            except:
                crop_error_count += 1
                print('There was an error cropping the image.')
                continue
            new_filename = path.basename(folder) + '--' + filename
            cropped.save(output_directory + '\\' + new_filename)
            crop_count += 1
    print('Done.')
    print('Scanned ' + str(file_count) + ' files.')
    print('There were ' + str(crop_count) + ' images cropped.')
    print('There were ' + str(crop_error_count) + ' crop errors.')
    print('There were ' + str(open_error_count) + ' open errors.')
    
source_crop(input_directory)
input()
