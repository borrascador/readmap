import sys
import json
from PIL import Image

def main():
    im = Image.open(sys.argv[1])
    pix = im.load()
    [width, height] = im.size

    print("Scanning {} pixels from input image".format(width*height))

    pixel_dict = {}
    for x in range(width):
        for y in range(height):
            pixel = pix[x,y]
            if pixel in pixel_dict:
                pixel_dict[pixel].append((x,y))
            else:
                pixel_dict[pixel] = []
    
    print("Found {} unique pixel color values".format(len(pixel_dict.keys())))
    
    over_100_counter = 0
    for pixel in pixel_dict:
        if len(pixel_dict[pixel]) > 100:
            over_100_counter += 1
    print("Found {} pixels with over 100 occurences".format(over_100_counter))

    over_1000_counter = 0
    for pixel in pixel_dict:
        if len(pixel_dict[pixel]) > 1000:
            over_1000_counter += 1
    print("Found {} pixels with over 1000 occurences".format(over_1000_counter))

    top_pixels = {}
    over_10000_counter = 0
    for pixel in pixel_dict:
        if len(pixel_dict[pixel]) > 10000:
            over_10000_counter += 1
            top_pixels[pixel] = len(pixel_dict[pixel])
    print("Found {} pixels with over 10000 occurences".format(over_10000_counter))
    print("\n Here is a list of the pixels with over 10000 occurences:")
    print(top_pixels)

if (len(sys.argv) > 0):
    main()
else:
    print('Image argument required.')
