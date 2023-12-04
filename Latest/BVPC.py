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
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
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
# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.sea_level_pressure = 1017.2



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


yellow = 0xC19C00
brightYellow = 0xF9F1A5
white = 0xffffff
red = 0xff0000
orange = 0xff5500
blue = 0x0000ff
pink = 0xff00ff
purple = 0x881798
brightPurple = 0xB4009E
white = 0xffffff
green = 0x16C60C
aqua = 0x00FFFF
grey = 0x4A4A4A


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

def ford_racing_startup():
    bitmap = displayio.OnDiskBitmap("/bbb.bmp")
     # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    # Create a Group to hold the TileGrid
    group = displayio.Group()
    # Add the TileGrid to the Group
    group.append(tile_grid)
    # Add the Group to the Display
    display.root_group = group


ford_racing_startup()
time.sleep(1)
gc.collect()

def boost_vision_startup():
    bitmap = displayio.OnDiskBitmap("/eee.bmp")
     # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    # Create a Group to hold the TileGrid
    group = displayio.Group()
    # Add the TileGrid to the Group
    group.append(tile_grid)
    # Add the Group to the Display
    display.root_group = group
    time.sleep(2)
    sick_font = bitmap_font.load_font("/InsertCoins-9.pcf")
    start_1 = ("PRESS START.")
    start_2 = ("            .")
    start_3 = ("             .")
    text_1 = label.Label(sick_font, text=start_1, color=red)
    text_1.anchor_point = (0.0, 0.0)
    text_1.anchored_position = (108, 130)
    group.append(text_1)
    time.sleep(.5)
    text_2 = label.Label(sick_font, text=start_2, color=red)
    text_2.anchor_point = (0.0, 0.0)
    text_2.anchored_position = (108, 130)
    group.append(text_2)
    time.sleep(.5)
    text_3 = label.Label(sick_font, text=start_3, color=red)
    text_3.anchor_point = (0.0, 0.0)
    text_3.anchored_position = (108, 130)
    group.append(text_3)
    time.sleep(.5)
    del sick_font
    
    
boost_vision_startup()
time.sleep(2.5)
gc.collect()

#fonts
my_font = bitmap_font.load_font("/InsertCoins-9.pcf")
scanline_30 = bitmap_font.load_font("/scanline-30.pcf")
sevenseg_30 = bitmap_font.load_font("7seg-30.pcf")
warningSign = bitmap_font.load_font("tables-20.pcf")
carParts = bitmap_font.load_font("CarParts-20.pcf")
arrowFont = bitmap_font.load_font("arrows.pcf")

#low boost indicators
text_f = (" ")
f_text = label.Label(scanline_30, text=text_f, color=green)
f_text.anchor_point = (0.0, 0.0)
f_text.anchored_position = (15, 4)
group.append(f_text)

text_fa = (" ")
fa_text = label.Label(scanline_30, text=text_fa, color=green)
fa_text.anchor_point = (0.0, 0.0)
fa_text.anchored_position = (30, 4)
group.append(fa_text)

text_fb = (" ")
fb_text = label.Label(scanline_30, text=text_fb, color=green)
fb_text.anchor_point = (0.0, 0.0)
fb_text.anchored_position = (45, 4)
group.append(fb_text)

#mid boost indicator
text_g = (" ")
g_text = label.Label(scanline_30, text=text_g, color=yellow)
g_text.anchor_point = (0.0, 0.0)
g_text.anchored_position = (60, 4)
group.append(g_text)


#high boost indicator
text_h = (" ")
h_text = label.Label(scanline_30, text=text_h, color=red)
h_text.anchor_point = (0.0, 0.0)
h_text.anchored_position = (105, 4)
group.append(h_text)

#warning sign
text_w = (" ")
w_text = label.Label(warningSign, text=text_w, color=red)
w_text.anchor_point = (0.0, 0.0)
w_text.anchored_position = (132, 100)
group.append(w_text)

#turbo icon
text_v = (" ")
v_text = label.Label(carParts, text=text_v, color=green)
v_text.anchor_point = (0.0, 0.0)
v_text.anchored_position = (112, 100)
group.append(v_text)

#data

text_x = ("PSI Label")
x_text = label.Label(terminalio.FONT, text=text_x, color=green)
x_text.anchor_point = (0.0, 0.0)
x_text.anchored_position = (120, 55)
group.append(x_text)

text_z = ("PSI Data")
z_text = label.Label(sevenseg_30, text=text_z, color=white)
z_text.anchor_point = (0.0, 0.0)
z_text.anchored_position = (20, 39)
group.append(z_text)
group.scale = 2

text_a = ("")
a_text = label.Label(my_font, text=text_a, color=brightPurple)
a_text.anchor_point = (0.0, 0.0)
a_text.anchored_position = (43, 106)
group.append(a_text)

text_al = ("Altitude")
al_text = label.Label(arrowFont, text=text_al, color=purple)
al_text.anchor_point = (0.0, 0.0)
al_text.anchored_position = (7, 100)
group.append(al_text)

text_b = ("voltage")
b_text = label.Label(my_font, text=text_b, color=brightYellow)
b_text.anchor_point = (0.0, 0.0)
b_text.anchored_position = (50, 87)
group.append(b_text)

text_bl = ("voltage")
bl_text = label.Label(carParts, text=text_bl, color=yellow)
bl_text.anchor_point = (0.0, 0.0)
bl_text.anchored_position = (7, 83)
group.append(bl_text)

text_c = ("status")
c_text = label.Label(my_font, text=text_c, color=grey)
c_text.anchor_point = (0.0, 0.0)
c_text.anchored_position = (106, 85)
group.append(c_text)

display.root_group = group
roundrect = RoundRect(2, 80, 100, 40, 5,outline=grey, stroke=1)
roundrect1 = RoundRect(2, 29, 156, 50, 5,outline=grey, stroke=1)
roundrect2 = RoundRect(103, 80, 55, 40, 5,outline=grey, stroke=1)
roundrect3 = RoundRect(2, 0, 156, 28, 5,outline=grey, stroke=1)
group.append(roundrect)
group.append(roundrect1)
group.append(roundrect2)
group.append(roundrect3)

#boost = ((chan.voltage * 9.48901) - bmp.pressure * .0145038)



while True:
    
    boost = ((chan.voltage * 9.48901) - bmp.pressure * .0145038)
    if boost >= .5:
        f_text.text = (">")
        v_text.text = ("l")
    else:
        f_text.text = (" ")
        v_text.text = (" ")
        gc.collect()
    if boost >= 5:
        fa_text.text = (">")
    else:
        fa_text.text = (" ")
        gc.collect()
    if boost >= 8:
        fb_text.text = (">")
    else:
        fb_text.text = (" ")
        gc.collect()
        
    if boost >=15:
        g_text.text = (">>>")
    else:
        g_text.text = (" ")
        gc.collect()
        
    if boost >=20:
        h_text.text = (">>>")
        w_text.text = ("I")
        
    else:
        h_text.text = (" ")
        w_text.text = (" ")
        gc.collect()
    if boost >=.5:
        a_text.text = "{:2.2f}PSI".format(boost)
    else:
        pass
    
    z_text.text = ("{:>5.2f}".format((chan.voltage * 9.48901) - bmp.pressure * .0145038))
    x_text.text = ("PSI")
    #a_text.text = ((chan.voltage * 9.48901) - bmp.pressure * .0145038)
    b_text.text = ("{:>5.3f}".format(chan.voltage))
    c_text.text = ("STATUS")
    bl_text.text = ("k")
    al_text.text = ("B")
    gc.collect()
    time.sleep(0.05)
