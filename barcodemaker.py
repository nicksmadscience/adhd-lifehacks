from io import BytesIO

from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image

import argparse
parser = argparse.ArgumentParser(
	prog = "Barcode Maker",
	description = "Generates sheets of barcodes for printing en masse."
)
parser.add_argument("prefix", help="All barcodes will be prefixd with this string")
parser.add_argument("start", help="Starting serial number", type=int)
parser.add_argument("--pad", help="Number of padded zeroes in serial", default=3, type=int)
parser.add_argument("--rows", default=7, type=int)
parser.add_argument("--cols", default=4, type=int)
parser.add_argument("--padding", help="Number of pixels between barcodes to make for easy paper-cutting", default=50, type=int)
parser.add_argument("--output", help="Filename to write to", default="")

args = parser.parse_args()

def makeBarcode(string):
	bytes = BytesIO()
	Code128(string, writer=ImageWriter()).write(bytes)
	return Image.open(bytes)

def makeSerial(prefix, num, pad):
	return "{prefix}{num:0{width}}".format(prefix=prefix, num=num, width=pad)

# setup a prototype for determining image dimensions
protoString = makeSerial(args.prefix, args.start + (args.rows * args.cols), args.pad)  # rows * cols to get the longest width and prevent overlap
protoImg = makeBarcode(protoString)

indWidth = protoImg.width
indHeight = protoImg.height
width = (indWidth + args.padding) * args.cols 
height = (indHeight + args.padding) * args.rows

canvas = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))

for row in range(0, args.rows):
	for col in range(0, args.cols):
		ser = (row * args.cols) + col + args.start
		str = (makeSerial(args.prefix, ser, args.pad))
		bc = makeBarcode(str)
		x = (col * indWidth) + (col * args.padding) + (args.padding >> 1)
		y = (row * indHeight) + (row * args.padding) + (args.padding >> 1)
		canvas.paste(bc, (x, y))
		print (ser, end=" ")
  
  
if args.output == "":
    output = "{start}__{end}.png".format(
        start=makeSerial(args.prefix, args.start, args.pad),
        end=makeSerial(args.prefix, args.start + (args.cols * args.rows) - 1, args.pad))
else:
    output = args.output
    
canvas.save(output)
print ("\nSaved barcodes as {output}.".format(output=output))