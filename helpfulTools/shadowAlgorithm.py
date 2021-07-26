import socket
import os
import matplotlib.pyplot as plt 
import matplotlib.image as img
from PIL import Image, ImageEnhance 
import datetime as dt
#Set Port Variables
TCP_IP = '192.168.1.158'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast=
counter = 0
#Infinite while loop, change to counter < n and uncomment counter to only do n amount of times
while(counter ==0):
  #counter= counter + 1;
  #Connect to Pi, waits until connection
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(5)
  (conn, addr) = s.accept()
  print(f"Connection from {addr} has been established!")
  print('Connection address:', addr)
  name = int(conn.recv(BUFFER_SIZE))
  print("received data:", name)  #conn.send(data)  # echo
  conn.close()
  #Run secure copy protocol command
  command = ("scp ~/id_rsa pi@192.168.1.250:Desktop/photobooth/image%s_*.jpg share" %name)
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
      logFile = open("share/trackerLog.txt", "a+")
      logFile.write("\nKept %s %s" %(addy, pic.max()))
      logFile.close()
      hourFile = open("share/timeofday2.txt", "a+")
      hourFile.write(",%s" %(hourofday))
      hourFile.close()
      folder = "promising"
      #change folder tp promising if over 40 and track it in huge values log
      if(pic.max() > 55):
        hugeFile = open("share/HugeValuesLog.txt", "a+")
        hugeFile.write("\nFound %s %s" %(addy, pic.max()))
        hugeFile.close()
        folder = "ultrapromising"
      max = pic.max()
      breakVar = False
      #search for highest value
      for height in range(0,pic.shape[0]):
        croppedimg = Image.open(addy).convert('L')
        imslice = croppedimg.crop((0, height, 1280, height + 1))
        cropaddy = ("%s_%s.png" %(name, x))
        imslice.save(cropaddy)
        snippic = img.imread(cropaddy)
        #imslice.close()
        #print(snippic.max())
        #if(snippic.max() > .1):
          #print(snippic.max())
        if(.00001 > abs(snippic.max() - (max/255))):
          print("Passed Check")
          for width in range(0,pic.shape[1]):
            if pic[height, width] == max:
              passValue = False
              threshold = 50;
              sumdiagonal = max
              sumdiagonal2 = max
              sumvertical = max
              sumhorizontal = max
              for counter in range(0, 10):
                sumdiagonal += pic[height + counter, width + counter]
                sumdiagonal += pic[height - counter, width - counter]
                sumdiagonal2 += pic[height + counter, width - counter]
                sumdiagonal2 += pic[height - counter, width + counter]
                sumvertical += pic[height + counter, width]
                sumvertical += pic[height - counter, width]
                sumhorizontal += pic[height, width + counter]
                sumhorizontal += pic[height, width - counter]
              if(sumdiagonal/20 > threshold):
                passValue = true
              if(sumdiagonal2/20 > threshold):
                passValue = true
              if(sumvertical/20 > threshold):
                passValue = true
              if(sumhorizontal/20 > threshold):
                passValue = true
              if(passValue)
                startWidth = width -30
                startHeight = height -30
                endWidth = width +30
                endHeight = height +30
                if(startWidth < 0):
                  startWidth = 0
                if(startHeight < 0):
                  startHeight = 0
                #Make sure not out of bounds
                if(endWidth > pic.shape[1]):
                  endWidth = pic.shape[1] # - 1
                if(endHeight > pic.shape[0]):
                  endHeight = pic.shape[0] # -1 
                cropimg = Image.open(addy)
                imsnap = cropimg.crop((startWidth, startHeight, endWidth, endHeight))
                location = ("share/snapshot/%s/image%s_%s_%s_%s.jpg" %(folder, name, x, width, height))
                imsnap.save(location)
                #Color Map
                colormapdata = img.imread(location)
                plt.figure(figsize=(7, 6)) 
                plt.pcolormesh(colormapdata, cmap = "hot")
                plt.colorbar()
                plt.savefig(("share/snapshot/%s/image%s_%s.png" %(folder, name, x)), bbox_inches='tight', pad_inches=0.0, dpi=200,)
                plt.close()
                breakVar = True
            if pic[height, width] == 0:
              width = width + 1
        height = height + 1
        os.remove(cropaddy)