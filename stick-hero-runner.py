'''The plan for How to: 
I can read the pixel row of 1212. Then filter by actually printing from 215th pixel. 
Then create a function to find the x co-ordinate of starting point of the stick. 
Create a function to find the x co-ordinate of start of the red box. 
Then maybe create a function to determine the distance between the two points. 

Do this first and let's see. 

'''

# Co-ordinate of start point : *, 1212 (is it consistent across bridges? no)
# Co-ordinate of red box : x, 1212
# Color of start point : 90, 62, 96
# Color of red box : 247, 27, 27
# (* - we have to figure out the start x-co-ordinate)
# Start line_pixel from 215th pixel(Finished)
# Combine the x_co-ordinates with the RGB values. 

from ppadb.client import Client
from PIL import Image
import numpy
import time

x_co = [i for i in range (1080)]
# print(x_co)

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]
while True:
	image = device.screencap()

	with open('myscreen.png', 'wb') as f:
	    f.write(image)

	image = Image.open('myscreen.png')
	image = numpy.array(image, dtype=numpy.uint8)
	original_pixel = [list(i[:3]) for i in image[1218]]
	#original_pixel = original_pixel[1079]
	line_pixel = {}
	for key in x_co:
		for value in original_pixel:
			line_pixel[key] = value
			original_pixel.remove(value)
			break
	#print(original_pixel)
	#print(line_pixel)
	gap_bridge = False
	start_of_bridge = False

	# To determine the starting pixel count of stick. 

	for key in line_pixel:
		if key != 0 and line_pixel[key] == [0, 0, 0] and not start_of_bridge:
			start_of_bridge = True
			#print("Looks like there is a gap behind us for like {} pixel(s). Don't look back!!!".format(key))
			#print("")
		elif key != 0 and line_pixel[key] != [0, 0, 0] and start_of_bridge:
			start_x = key
			print("I think we could start at the {}th pixel. ".format(key)) 
			break

	for key in line_pixel:
		if line_pixel[key] == [247, 27, 27]:
			start_red = key
			print("It's a good practice to land at the red box which is at {}th pixel. ".format(key))
			break

	distance =(( start_red - start_x) / 100) * 101.40

	'''
	if distance < 200:
		distance += 20
	elif 200 > distance > 400:
		distance += 15
	elif 400 > distance > 600:
		distance += 6
	else:
		distance = distance
	'''
	print(distance)
	device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')
	time.sleep(3)
	print("")
	print("")
	print("Starting again!!!")

