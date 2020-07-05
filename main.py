import pytesseract
import os
import re
import math
from PIL import Image, ImageEnhance, ImageOps

custom_config = '--psm 4'
path = '/tests'
filepaths = [os.path.join(r, file) for r, d, f in os.walk(os.getcwd() + path) for file in f]
filepaths = [x for x in filepaths if x.endswith('.png')]
for f in filepaths:
    testpath = '/'.join(f.split('/')[-2:])
    print(testpath)
    textpath = ''.join(f.split('.')[0:-1]) + '.txt'
    textfile = open(textpath, 'r')
    text = textfile.read()

    im = Image.open(f)
    enhancer = ImageEnhance.Color(ImageOps.invert(im.convert('RGB')))
    im = enhancer.enhance(0)

    pixels = im.load()

    for i in range(im.size[0]):    # for every col:
        for j in range(im.size[1]):    # For every row
            if pixels[i,j][0] > 180: # set the colour accordingly
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0, 0, 0)

    data = pytesseract.image_to_string(im, config = custom_config)
    prettydata = re.sub(r'\s+', ' ', data)

    cmparr = []
    for i in range(len(text)):
        if i < len(prettydata):
            cmparr.append(1 if text[i] == prettydata[i] else 0)
    
    approxprcnt = (sum(cmparr) / len(text) * 100)
    print('{:.2f}%'.format(approxprcnt))
    print(text.lstrip())
    print(prettydata, end='\n\n')