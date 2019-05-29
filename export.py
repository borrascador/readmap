import sys
import statistics
import json
import re
from PIL import Image

def main():
    source = sys.argv[1]
    threshold = int(sys.argv[2], 10)
    color_count = 2
    do_export = sys.argv[3].find('x') > -1
    do_display = sys.argv[3].find('d') > -1
    output_file = len(sys.argv) > 4 and sys.argv[4] if do_export else ""

    src = Image.open(source)
    src_pixels = src.load()
    [width, height] = src.size

    print("Scanning {} pixels from input image".format(width*height))

    pixel_dict = {}
    for x in range(width):
        for y in range(height):
            pixel = src_pixels[x,y]
            if pixel in pixel_dict:
                pixel_dict[pixel].append((x,y))
            else:
                pixel_dict[pixel] = []
    
    unique_input_colors = len(pixel_dict.keys())

    print("Found {} unique pixel color values".format(unique_input_colors))
    if len(pixel_dict.keys()) <= color_count:
        print("Source image is already in {} colors or less.".format(color_count))
        return

    # Use number of desired regions to expand
    sorted_lengths = sorted(pixel_dict, key=lambda k: len(pixel_dict[k]), reverse=True)
    top_pixels = sorted_lengths[:color_count]
    combined_occurences = sum([len(pixel_dict[top_pixels[x]]) for x in range(color_count)])
    share = combined_occurences / (width * height)

    print("Found {} pixels with {} combined occurences ({} share)".format(color_count, combined_occurences, share))
    print(top_pixels)

    out = Image.new(src.mode, src.size)
    out_pixels = out.load()
    out_pixel_dict = {}
    for x in range(width):
        for y in range(height):
            blended_pixel = blend2colors(top_pixels[0], top_pixels[1], src_pixels[x,y], threshold)
            out_pixels[x,y] = blended_pixel
            if blended_pixel in out_pixel_dict:
                out_pixel_dict[blended_pixel].append((x,y))
            else:
                out_pixel_dict[blended_pixel] = [(x,y)]
            
    unique_output_colors = len(out_pixel_dict.keys())
    print("{} unique output colors remaining from {} original colors".format(unique_output_colors, unique_input_colors))

    if do_display:
        out.show()

    if do_export and output_file:
        out.save(output_file)
        print("Exported as {}".format(output_file))

def blend2colors(color1, color2, pixel, threshold):
    if (pixel == color1):
        return color1
    if (pixel == color2):
        return color2
    color1diff = diff2colors(color1, pixel)
    color2diff = diff2colors(color2, pixel)
    if (color1diff < threshold and color1diff < color2diff):
        return color1
    elif (color2diff < threshold and color2diff < color1diff):
        return color2
    else:
        return pixel

def diff2colors(c1, c2):
    return sum([abs(c1[x] - c2[x]) for x in range(4)])

if (len(sys.argv) > 0):
    main()
else:
    print('Image argument required.')
