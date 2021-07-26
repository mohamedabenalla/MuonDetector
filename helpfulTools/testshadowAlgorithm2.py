import numpy as np
from PIL import Image
import matplotlib.image as img
from PIL import Image
import os 
import math
addy1 = "image16442_13.jpg"
placeholder = Image.open(addy1).convert('L')
placeholder.save(addy1)
image = img.imread(addy1)

imageaddys = [addy1]
#for batch in range(4000,12000):
#	for x in range(0, 20):
#addy = ("share/image%s_%s.jpg" %(batch, x))
#if (os.path.exists(addy)):
#print(addy)
#imager = Image.open(addy).convert('L')
#imsnap = imager.crop((150, 0, 1150, 720))
#addy = ("cropfolder/share/_noncroppedimage%s_%s.jpg" %(batch, x))
			#imsnap.save(addy)
#imager.save(addy)
			#imager2 = Image.open(addy).convert('L')
			#imager2.save(addy)
#imageaddys.append(addy)	

array = np.zeros(921600)
array = np.reshape(array, (720, 1280))
verymax = 0
for addy in imageaddys:
	pic = img.imread(addy)
	#if(pic.max() >40):
	if(pic.max() >0):
			print('Maximum RGB value in this image {}'.format(pic.max()))
			folder = open("cropfolder/share/newcroppedvaluelog.txt", "a+")
			folder.write("\nFound %s %s" %(addy, pic.max()))
			folder.close()
			if(pic.max() > 55):
					hugeFile = open("cropfolder/share/newcroppedHugeValuesLog.txt", "a+")
					hugeFile.write("\nFound %s %s" %(addy, pic.max()))
					hugeFile.close()
			max = pic.max()
			breakVar = False
			#search for highest value
			for height in range(0,pic.shape[0]):
					croppedimg = Image.open(addy).convert('L')
					imslice = croppedimg.crop((0, height, 1280, height + 1))
					cropaddy = ("the%sx%s.png" %(max, height))
					imslice.save(cropaddy)
					snippic = img.imread(cropaddy)
					if(.00001 > abs(snippic.max() - (max/255))):
							for width in range(0,pic.shape[1]):
									if pic[height, width] == max:
										passValue = False
										threshold = 50;
										for angle in range (0,180):
											sumdiagonal = max
											for counter in range(0, 10):
										  		sumdiagonal += int(pic[height + int(math.cos(angle) * counter), width + int(math.sin(angle) * counter)])
										  		sumdiagonal += int(pic[height + int(math.cos(angle) * counter), width + int(math.sin(angle) * counter)])
											if(sumdiagonal/21 > threshold):
										  		passValue = True
										if(passValue):
											print("found")
					os.remove(cropaddy)