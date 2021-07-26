from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
# Below code does the authentication
# part of the code
gauth = GoogleAuth()
  
# Creates local webserver and auto
# handles authentication.
gauth.LocalWebserverAuth()       
drive = GoogleDrive(gauth)
#Open list
#Reiterate through uploading each
uploadFile = drive.CreateFile({'parents': [{'id': "changethis"}], 'title':("image%s_%s_%s,_%s.png" %(name, x, width, height))} )
uploadFile.SetContentFile(colormaplocation)
uploadFile.Upload()
