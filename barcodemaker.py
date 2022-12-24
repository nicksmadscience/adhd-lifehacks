from io import BytesIO

from barcode import Code128
from barcode.writer import SVGWriter


from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

import argparse
parser = argparse.ArgumentParser(
	prog = "Barcode Maker",
	description = "Generates sheets of barcodes for printing en masse."
)
parser.add_argument("prefix", help="All barcodes will be prefixd with this string")
parser.add_argument("start", help="Starting serial number", type=int)
parser.add_argument("--pad", help="Number of padded zeroes in serial", default=3, type=int)
parser.add_argument("--rows", default=10, type=int)
parser.add_argument("--cols", default=5, type=int)
parser.add_argument("--hgap", help="Number of horizontal units between barcodes to make for easy paper-cutting", default=120, type=int)
parser.add_argument("--vgap", help="Number of vertical units between barcodes to make for easy paper-cutting", default=80, type=int)
parser.add_argument("--output", help="Filename to write to", default="")

args = parser.parse_args()

def makeBarcode(string):
	with open("temp.svg", "wb") as f:
		Code128(string, writer=SVGWriter()).write(f)
	return svg2rlg("temp.svg")

def makeSerial(prefix, num, pad):
	return "{prefix}{num:0{width}}".format(prefix=prefix, num=num, width=pad)

if args.output == "":
    output = "{start}__{end}.pdf".format(
        start=makeSerial(args.prefix, args.start, args.pad),
        end=makeSerial(args.prefix, args.start + (args.cols * args.rows) - 1, args.pad))
else:
    output = args.output

my_canvas = canvas.Canvas(output)

for row in range(0, args.rows):
	for col in range(0, args.cols):
		ser = (row * args.cols) + col + args.start
		str = (makeSerial(args.prefix, ser, args.pad))
		bc = makeBarcode(str)
		x = 0 + (col * args.hgap)
		y = 750 - (row * args.vgap)
		drawing = svg2rlg("temp.svg")
		renderPDF.draw(drawing, my_canvas, x, y)
  
my_canvas.save()
print ("Saved barcodes as {output}.".format(output=output))