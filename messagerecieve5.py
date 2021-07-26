import socket
import os
import matplotlib.pyplot as plt 
import matplotlib.image as img
from PIL import Image, ImageEnhance 
import datetime as dt
import math
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
#Set Port Variables
TCP_IP = '192.168.1.158'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast=
counter = 0
# Below code does the authentication
# part of the code
gauth = GoogleAuth()
  
# Creates local webserver and auto
# handles authentication.
gauth.LocalWebserverAuth()       
drive = GoogleDrive(gauth)

#Infinite while loop, change to counter < n and uncomment counter to only do n amount of times
while(counter <40):
  counter+=1
  #counter= counter + 1;
  #Connect to Pi, waits until connection
  print("waiting..")
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(5)
  (conn, addr) = s.accept()
  print(f"Connection from {addr} has been established!")
  print('Connection address:', addr)
  name = int(conn.recv(BUFFER_SIZE))
  print("received data:", name)  #conn.send(data)  # echo
  conn.send(b'1')
  conn.close()
  #Run secure copy protocol command
  command = ("scp ~/id_rsa pi@%s:Desktop/photobooth/image%s_*.jpg share" %("192.168.1.159", name))
  print(command)
  os.system(command)
  hourofday = dt.datetime.now().hour
  batchsize = 20
  for x in range(batchsize):
    #code that keeps track of how many images in total
    batchFile = open("share/timeofdaytotal2.txt", "a+")
    batchFile.write(",%s" %(hourofday))
    batchFile.close()
    #Grab Image from address
    addy = ("share/image%s_%s.jpg" %(name, x))
    imager = Image.open(addy).convert('L') #greyscale from .convert('L')
    imager.save(addy)  
    pic = img.imread(addy) 
    #print('Maximum RGB value in this image {}'.format(pic.max()))
    #Delete all images with brightness value under 40 and keep all over 40
    if(pic.max() < 40): #pic.max() is highest value
      os.remove(addy)
      logFile = open("share/imageLog.txt", "a+")
      logFile.write("\nDeleted %s %s" %(addy, pic.max()))
      logFile.close()
    else:
      #Commented code was the code I used to enhance images from the computer
      #enhanceValue = 255/pic.max();
      #enhancer = ImageEnhance.Brightness(imager)
      #enhanced_im = enhancer.enhance(enhanceValue)
      #if(pic.max() < 41):
        #imagemod = enhanced_im.point(lambda i: i > 10 and i < 120 and 255)
        #imagemod2 = enhanced_im.point(lambda i: i + 60)
        #enhanced_im.paste(imagemod2, None, imagemod)
      #enhancer = ImageEnhance.Brightness(imager)
      #enhanced_im = enhancer.enhance(enhanceValue)
      #print(enhanceValue)
      #enhanced_im.save(addy)
      print('Maximum RGB value in this image {}'.format(pic.max()))
      #tracking actions and time of day
      #logFile = open("share/trackerLog.txt", "a+")
      #logFile.write("\nKept %s %s" %(addy, pic.max()))
      #logFile.close()
      hourFile = open("share/timeofday2.txt", "a+")
      hourFile.write(",%s" %(hourofday))
      hourFile.close()
      folder = "promising"
      #change folder tp promising if over 40 and track it in huge values log
      #f(pic.max() > 55):
        #hugeFile = open("share/HugeValuesLog.txt", "a+")
        #hugeFile.write("\nFound %s %s" %(addy, pic.max()))
        #hugeFile.close()
        #folder = "ultrapromising"
      max = pic.max()
      breakVar = False
      #search for highest value
      for height in range(0,pic.shape[0]):
        croppedimg = Image.open(addy).convert('L')
        imslice = croppedimg.crop((0, height, 1280, height + 1))
        cropaddy = ("%s_%s.png" %(name, x))
        imslice.save(cropaddy)
        snippic = img.imread(cropaddy)
        if(.00001 > abs(snippic.max() - (max/255))):
                      for width in range(30,1179):
                          if pic[height, width] >= 30:
                            passValue = False
                            threshold = 18;
                            folder = "shadowpromising"
                            for angle in range (0,180):
                              sumdiagonal = max
                              for counting in range(0, 10):
                                  sumdiagonal += int(pic[height + int(math.cos(angle) * counting), width + int(math.sin(angle) * counting)])
                                  sumdiagonal += int(pic[height - int(math.cos(angle) * counting), width - int(math.sin(angle) * counting)])
                              print((sumdiagonal/21))
                              if(sumdiagonal/21 > threshold):
                                  passValue = True
                                  perpangle = angle + 90
                                  for counting in range(0, 10):
                                    sumdiagonal += int(pic[height + int(math.cos(perpangle) * counting), width + int(math.sin(perpangle) * counting)])
                                    sumdiagonal += int(pic[height - int(math.cos(perpangle) * counting), width - int(math.sin(perpangle) * counting)])
                              if(sumdiagonal/25 > threshold):
                                  folder = "shadowultrapromising"
                              #print(sumdiagonal)
                            if(passValue):
                              startWidth = width -20
                              startHeight = height -20
                              endWidth = width +20
                              endHeight = height +20
                              if(startWidth < 0):
                                startWidth = 0
                              if(startHeight < 0):
                                startHeight = 0
                              cropimg = Image.open(addy)
                              imsnap = cropimg.crop((startWidth, startHeight, endWidth, endHeight))
                              location = ("share/snapshot/%s/image%s_%s_%s_%s_unfiltered.jpg" %(folder, name, x, width, height))
                              imsnap.save(location)
                              #Color Map
                              colormapdata = img.imread(location)
                              plt.figure(figsize=(7, 6)) 
                              plt.pcolormesh(colormapdata, cmap = "hot")
                              plt.colorbar()
                              colormaplocation = ("share/snapshot/%s/image%s_%s_%s_%s.png" %(folder, name, x, width, height))
                              plt.savefig(colormaplocation, bbox_inches='tight', pad_inches=0.0, dpi=200,)
                              plt.close()
                              print(colormaplocation)
                              if(sumdiagonal/25 > threshold):
                                uploadFile = drive.CreateFile({'parents': [{'id': "15rcCIsgj8atpi68RtZwDjV5VOGwVfeTY"}], 'title':("image%s_%s_%s_%s.png" %(name, x, width, height))} )
                                uploadFile.SetContentFile(colormaplocation)
                                uploadFile.Upload()
                                #add file to list instead
        height = height + 1
        os.remove(cropaddy)