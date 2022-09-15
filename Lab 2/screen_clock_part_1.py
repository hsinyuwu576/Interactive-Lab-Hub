import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Set buttom
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


x = 60
y = 40
rect_w = 110
rect_h = 40
vx = 0
vy = 0
ax = 0
ay = 0


def UpdateAcc():
    global ax, ay

    tmpx = 0
    tmpy = 0
    if not buttonA.value:
        tmpx += 8
        tmpy += 8
        draw.rectangle((0, height - 1, width, height - 1), outline = "#EA0000")
        draw.rectangle((width - 1, 0, width - 1, height), outline = "#EA0000")
    if not buttonB.value:
        tmpx -= 8
        tmpy -= 8
        draw.rectangle((0, 0, width, 0), outline = "#009100")
        draw.rectangle((0, 0, 0, height), outline = "#009100")

    ax = tmpx
    ay = tmpy


def UpdateLoc():
    global x, y, vx, vy
    vx += ax
    vy += ay
    x += vx
    y += vy

    if x + rect_w + 1 > width:
        vx *= -0.8
        x = width - rect_w - 1
    elif x < 0:
        vx *= -0.8
        x = 0

    if y + rect_h + 1 > height:
        vy *= -0.8
        y = height - rect_h - 1
    elif y < 0:
        vy *= -0.8
        y = 0


def DrawClock():
    draw.rectangle((x, y, x + rect_w, y + rect_h), outline = "#FFFFFF", fill = 0)
    draw.text((x + 3, y + 4), time.strftime("%m/%d/%Y"), font = font, fill = "#FFFFFF")
    draw.text((x + 3, y + 19), time.strftime("%H:%M:%S"), font = font, fill = "#FFFFFF")

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    UpdateAcc()
    UpdateLoc()
    DrawClock()

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.01)
