##MErges all images together to try to detect propensity in certain locations to avoid bias
from PIL import Image
import numpy as np
import matplotlib.image as img
from PIL import Image
import os 
#imager = Image.open(addy).convert('L')
addy1 = "image33_5.jpg"
addy2= "image33_8.jpg"
image = img.imread(addy1) 
image2 = img.imread(addy2)
#r, g, b = image.split()
#print(b)
images = [image]
for batch in range(10000,12719):
	for x in range(0, 20):
		addy = ("share/image%s_%s.jpg" %(batch, x))
		if (os.path.exists(addy)):
			imager = Image.open(addy).convert('L')
			imager.save(addy)
			images.append(img.imread(addy))	

array = np.zeros(921600)
array = np.reshape(array, (720, 1280)) 
print(array.ndim)
for height in range(0,719):
	for width in range(0,1279):
		for pic in images:
			array[height, width] += pic[height, width]
data = Image.fromarray(array) 
data = data.convert('L')