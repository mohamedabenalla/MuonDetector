# MuonDetector
Raspberry Pi Project to try to detect muon particles

Result: Detected about 3 potential particles a week (out of 201,600 images taken a week)

(Estimated actual particle count is about 1 a week)

Instructions

- Upload messagerecieve python script to computer to anaylze incoming images from pi
- Upload launcher.sh and info.py to raspberry pi to schedule and take images
- Configure firewall within computer and network to allow for communication within the network
- Configure Raspberry Pi to allow for external communication
- Set up Raspberry Pi Camera adding a scintillator over the camera or substitutes such as reflective tape
- Set up Cron Scheduling with launcher.sh to execute bash script every minute

Additional

-My Personal Research Paper into Muon Detection is included in Adjacent Research
