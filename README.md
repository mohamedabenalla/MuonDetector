# MuonDetector
Raspberry Pi Project to try to detect muon particles

Result: Detected about 2 particles a week (Estimated actual particle count is about 1 a week)

Instructions

- Upload messagerecieve python script to computer to anaylze incoming images from pi
- Upload launcher.sh and info.py to raspberry pi to schedule and take images
- Configure firewall within computer and network to allow for communication within the network
- Configure Raspberry Pi to allow for external communication
- Set up Raspberry Pi Camera adding a scintillator or substitutes such as reflective tape
- Set up Cron Scheduling with launcher.sh to execute bash script every minute
