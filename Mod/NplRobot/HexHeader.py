from microbit import *
import microbit
import math, ustruct
# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04
RESET              = 0x00

class PCA9685():
    """PCA9685 PWM LED/servo controller."""

    def __init__(self, i2c, address=PCA9685_ADDRESS):
        """Initialize the PCA9685."""
        self.address = address
        i2c.write(self.address, bytearray([MODE1, RESET])) # reset not sure if needed but other libraries do it
        self.set_all_pwm(0, 0)
        i2c.write(self.address, bytearray([MODE2, OUTDRV]))
        i2c.write(self.address, bytearray([MODE1, ALLCALL]))
        sleep(5)  # wait for oscillator
        i2c.write(self.address, bytearray([MODE1])) # write register we want to read from first
        mode1 = i2c.read(self.address, 1)
        mode1 = ustruct.unpack('<H', mode1)[0]
        mode1 = mode1 & ~SLEEP  # wake up (reset sleep)
        i2c.write(self.address, bytearray([MODE1, mode1]))
        sleep(5)  # wait for oscillator

    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        # print('Setting PWM frequency to {0} Hz'.format(freq_hz))
        # print('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = int(math.floor(prescaleval + 0.5))
        # print('Final pre-scale: {0}'.format(prescale))
        i2c.write(self.address, bytearray([MODE1])) # write register we want to read from first
        oldmode = i2c.read(self.address, 1)
        oldmode = ustruct.unpack('<H', oldmode)[0]
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        i2c.write(self.address, bytearray([MODE1, newmode]))  # go to sleep
        i2c.write(self.address, bytearray([PRESCALE, prescale]))
        i2c.write(self.address, bytearray([MODE1, oldmode]))
        sleep(5)
        i2c.write(self.address, bytearray([MODE1, oldmode | 0x80]))

    def set_pwm(self, channel, on, off):
        on = int(on)
        off = int(off)
        """Sets a single PWM channel."""
        if on is None or off is None:
            i2c.write(self.address, bytearray([LED0_ON_L+4*channel])) # write register we want to read from first
            data = i2c.read(self.address, 4)
            return ustruct.unpack('<HH', data)
        i2c.write(self.address, bytearray([LED0_ON_L+4*channel, on & 0xFF]))
        i2c.write(self.address, bytearray([LED0_ON_H+4*channel, on >> 8]))
        i2c.write(self.address, bytearray([LED0_OFF_L+4*channel, off & 0xFF]))
        i2c.write(self.address, bytearray([LED0_OFF_H+4*channel, off >> 8]))

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        i2c.write(self.address, bytearray([ALL_LED_ON_L, on & 0xFF]))
        i2c.write(self.address, bytearray([ALL_LED_ON_H, on >> 8]))
        i2c.write(self.address, bytearray([ALL_LED_OFF_L, off & 0xFF]))
        i2c.write(self.address, bytearray([ALL_LED_OFF_H, off >> 8]))




def GetImage_Str(matrix_sequence_str):
	"""
		convert a str to Image
		matrix_sequence_str like this: "0010000100001000010000111"
		return "00900:00900:00900:00900:00999"
	"""
	str_len = len(matrix_sequence_str)
	if str_len == 0:
		return "00000:00000:00000:00000:00000"
	if str_len != 25 :
		return "99999:99999:99999:99999:99999"
	result = ""
	for i in range(str_len):
		c = matrix_sequence_str[i]
		input_c = c
		if input_c != "0":
			input_c = "9" # highlight with max level 
		index = i + 1
		if index % 5 == 0:
			result += input_c
			if index < str_len:
				result += ":"
		else:
			result += input_c
	return result

def GetImage(matrix_sequence_str):
	return microbit.Image(GetImage_Str(matrix_sequence_str))


pca = PCA9685(microbit.i2c)
pca.set_pwm_freq(60)


def microbit_servo(bone_name, axis, value, channel):
    if(not pca):
        return
    channel = int(channel)
    us = (value * 1800 / 180 + 600) # 0.6 ~ 2.4
    pwm = us * 4096 / 20000
    pca.set_pwm(channel, 0, pwm)

def microbit_sleep(time):
    microbit.sleep(time)

def microbit_is_pressed(btn):
    if(btn == "A"):
        return microbit.button_a.is_pressed()
    elif(btn == "B"):
        return microbit.button_b.is_pressed()

def microbit_display_show(matrix_sequence_str):
    img = GetImage(matrix_sequence_str)
    microbit.display.show(img)

def microbit_display_scroll(txt):
    microbit.display.scroll(txt)

def microbit_display_clear():
    microbit.display.clear()
