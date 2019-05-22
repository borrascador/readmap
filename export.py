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
    
    top_pixels = get_stats(pixel_dict, [100000])

    out = Image.new(im.mode, im.size)
    pixels_out = out.load()
    for pixel in top_pixels.keys():
        for coord in top_pixels[pixel]:
            pixels_out[coord] = pixel

    out.show()

def get_stats(pixel_dict, threshold_array):
    print("Found {} unique pixel color values".format(len(pixel_dict.keys())))

    threshold_array.sort()
    threshold_dict = { x: {} for x in threshold_array }

    for threshold in threshold_array:
        for pixel in pixel_dict:
            if len(pixel_dict[pixel]) > threshold:
                threshold_dict[threshold][pixel] = pixel_dict[pixel]
        count = len(threshold_dict[threshold].keys())
        print("Found {} pixels with over {} occurences".format(count, threshold))

    top_threshold = threshold_array[-1]
    print("Here is a list of the pixels with over {} occurences:".format(top_threshold))
    top_pixels = threshold_dict[top_threshold]
    print({ x: len(top_pixels[x]) for x in top_pixels})

    return top_pixels

if (len(sys.argv) > 0):
    main()
else:
    print('Image argument required.')
