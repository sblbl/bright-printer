import os
import cups  # if using rpi pip uninstall pycups and pip install cups

# import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from random import randint

conn = cups.Connection()
printers = conn.getPrinters()
# print(printers)
printer = printers["Xprinter_XP_420B"]
# printer = printers['Xprinter-XP-420B']


def writeRecord(value, i):
    # if there is no file create one
    if not os.path.isfile("records.tsv"):
        with open("records.tsv", "w") as f:
            f.write("code\tprediction\n")

    with open("records.tsv", "a") as f:
        f.write(f"{i}\t{value}\n")


def printReceipt(value, i):
    print("printing")

    # make i to be 4 digits
    i = str(i).zfill(4)
    writeRecord(value, i)

    base_img = Image.open("scontrino.png")
    im = ImageDraw.Draw(base_img)
    font = ImageFont.truetype("VT323-Regular.ttf", 100)
    im.text(
        (429, 1400),
        str(i),
        font=font,
        fill=(0, 0, 0),
    )
    im.text((578, 1484), str(value), font=font, fill=(0, 0, 0))
    # base_img.show()

    base_img.save("temp.png")

    # print by filling all the space
    conn.printFile("Xprinter_XP_420B", "temp.png", "image", {"fit-to-page": "true"})
