from picamera import PiCamera
from time import sleep
from PIL import Image, ImageEnhance
import os
import socket
#Set destination
TCP_IP = '192.168.1.158'
TCP_PORT = 5005
BUFFER_SIZE = 20
counterFile = open("imageCounter.txt", "r")
#Get Batch Number to name file
batch = int(counterFile.read())
print(batch)
counterFile.close()
camera = PiCamera()
camera.shutter_speed = 100
counter = 0
while (counter < 20):
	camera.capture('/home/pi/Desktop/photobooth/image%s_%s.jpg' %(batch, counter))
	#Commented code was to enhance images
	#im = Image.open('/home/pi/Desktop/photobooth/image%s_%s.jpg' %(batch, counter))
	#enhancer = ImageEnhance.Contrast(im)
	#im_output = enhancer.enhance(20)
	#im_output.save('/home/pi/Desktop/photobooth/image%s_%s.jpg' %(batch, counter))
	counter+= 1
	sleep(1)
#Connect to port and send data
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(str(batch))
#Write new file name
counterFile = open("imageCounter.txt", "w")
batch = batch + 1
counterFile.write(str(batch))
counterFile.close()
sleep(5)
print(s.recv(20))
#Helps keep storage in check by deleting old photos
os.system("sudo rm -r /home/pi/Desktop/photobooth")
os.system("sudo mkdir /home/pi/Desktop/photobooth")

