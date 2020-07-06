# Stick Hero Runner. Created by Harish Palanivel. 

from ppadb.client import Client
from PIL import Image
import numpy
import time



# For counting the pixels in the column. 
x_co = [i for i in range (1080)]


# Connection with the mobile through ADB. 
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()
device = devices[0]

while True:
	# Capturing the screen for processing. 
	image = device.screencap()
	with open('myscreen.png', 'wb') as f:
	    f.write(image)
	image = Image.open('myscreen.png')
	image = numpy.array(image, dtype=numpy.uint8)

	# Processing. 
	pixels = [list(i[:3]) for i in image[1218]]
	line_pixel = {}
	for key in x_co:
		for value in pixels:
			line_pixel[key] = value
			pixels.remove(value)
			break
	gap_bridge = False
	start_of_bridge = False

	# To determine the starting pixel, starting pixel of red box for "PERFECT" landing!
	# There is a weird line in the first row of pixels, so I've made it to account for those also. 
	for key in line_pixel:
		if key != 0 and line_pixel[key] == [0, 0, 0] and not start_of_bridge:
			start_of_bridge = True
		elif key != 0 and line_pixel[key] != [0, 0, 0] and start_of_bridge:
			start_x = key
			print("I think I could start at the {}th pixel. ".format(key)) 
			break
	for key in line_pixel:
		if line_pixel[key] == [247, 27, 27]:
			start_red = key
			print("I think the red box is at {}th pixel. ".format(key))
			break

	distance =(( start_red - start_x) / 100) * 101.40

	print("The distance is calculated at {}".format(distance))
	device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')
	time.sleep(3)
	print("")
	print("")
	print("Starting again!!!")

