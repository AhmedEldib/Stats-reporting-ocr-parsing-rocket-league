import cv2 
import pytesseract
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image, ImageEnhance, ImageOps

im = Image.open('Capture.png')
enhancer = ImageEnhance.Color(ImageOps.invert(im))
im = enhancer.enhance(0)

pixels = im.load() # create the pixel map

for i in range(im.size[0]):    # for every col:
    for j in range(im.size[1]):    # For every row
        if pixels[i,j][0] > 127: # set the colour accordingly
            pixels[i, j] = (255, 255, 255)
        else:
            pixels[i, j] = (0, 0, 0)

im.show()

# Adding custom options
custom_config = '--psm 7'

x = pytesseract.image_to_string(im, config=custom_config)
print(x)