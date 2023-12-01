import gc
import math
import time
import displayio
import picodvi
import board
import framebufferio
import vectorio
import terminalio
import simpleio
import busio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label, wrap_text_to_lines
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_bmp3xx

displayio.release_displays()

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.sea_level_pressure = 1017.2
bmp390_mode(bmp390, mode='lowpower')
bmp390.pressure_oversampling = 16
bmp390.temperature_oversampling = 2
bmp390.filter_coefficient = 4

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)



# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

# check for DVI Feather
if 'CKP' in dir(board):
    fb = picodvi.Framebuffer(320, 240,
        clk_dp=board.CKP, clk_dn=board.CKN,
        red_dp=board.D0P, red_dn=board.D0N,
        green_dp=board.D1P, green_dn=board.D1N,
        blue_dp=board.D2P, blue_dn=board.D2N,
        color_depth=8)
# otherwise assume Pico
else:
    fb = picodvi.Framebuffer(320, 240,
        clk_dp=board.GP12, clk_dn=board.GP13,
        red_dp=board.GP10, red_dn=board.GP11,
        green_dp=board.GP8, green_dn=board.GP9,
        blue_dp=board.GP6, blue_dn=board.GP7,
        color_depth=8)
display = framebufferio.FramebufferDisplay(fb)

bitmap = displayio.Bitmap(display.width, display.height, 3)


yellow = 0xcccc00
white = 0xffffff
red = 0xff0000
orange = 0xff5500
blue = 0x0000ff
pink = 0xff00ff
purple = 0x5500ff
white = 0xffffff
green = 0x00ff00
aqua = 0x125690


palette = displayio.Palette(3)
palette[0] = 0x000000 # black
palette[1] = white
palette[2] = yellow

palette.make_transparent(0)

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group()

def clean_up(group_name):
    for _ in range(len(group_name)):
        group_name.pop()
    gc.collect()

def run_before_loop():
    bitmap = displayio.OnDiskBitmap("/blinka.bmp")
     # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    # Create a Group to hold the TileGrid
    group = displayio.Group()
    # Add the TileGrid to the Group
    group.append(tile_grid)
    # Add the Group to the Display
    display.root_group = group
    time.sleep(2.0)

time.run_before_loop()

gc.collect()
my_font = bitmap_font.load_font("/Helvetica-Bold-16.pcf")
text_sample = "The quick brown fox jumps over the lazy dog."
text_sample = "\n".join(wrap_text_to_lines(text_sample, 28))
text_area = label.Label(my_font, text="Custom Font", color=white)
text_area.anchor_point = (50, 25)
text_area.anchored_position = (0, 0)

sample_text = label.Label(my_font, text=text_sample)
sample_text.anchor_point = (0.5, 0.5)
sample_text.anchored_position = (display.width / 3, display.height / 3)

group.append(text_area)
group.append(sample_text)

clean_up(group)

del my_font
gc.collect()

text_x = ("PSI Label")
x_text = label.Label(terminalio.FONT, text=text_x, color=green)
x_text.anchor_point = (0.0, 0.0)
x_text.anchored_position = (90, 25)
group.append(x_text)

text_z = ("PSI Data")
z_text = label.Label(terminalio.FONT, text=text_z, color=white)
z_text.anchor_point = (0.0, 0.0)
z_text.anchored_position = (50, 25)
group.append(z_text)
group.scale = 2

text_y = ("PSI Ambient")
y_text = label.Label(terminalio.FONT, text=text_y, color=aqua)
y_text.anchor_point = (0.0, 0.0)
y_text.anchored_position = (18, 65)
group.append(y_text)

text_a = ("Altitude")
a_text = label.Label(terminalio.FONT, text=text_a, color=orange)
a_text.anchor_point = (0.0, 0.0)
a_text.anchored_position = (18, 85)
group.append(a_text)

text_b = ("voltage")
b_text = label.Label(terminalio.FONT, text=text_b, color=yellow)
b_text.anchor_point = (0.0, 0.0)
b_text.anchored_position = (18, 45)
group.append(b_text)

display.root_group = group

while True:
    z_text.text = ("{:>5.3f}".format((chan.voltage * 9.48901) - bmp.pressure * .0145038))
    x_text.text = ("PSI")
    y_text.text = ("Ambient PSI:{:6.1f}".format(bmp.pressure * .0145038))
    a_text.text = ('Altitude Ft: {} '.format(bmp.altitude * 3.28084))
    b_text.text = ("MAP Voltage: {:>5.3f}v".format(chan.voltage))
    time.sleep(0.05)
