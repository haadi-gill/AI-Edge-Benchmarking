# Raspberry Pi Zero

### Operating System:
Raspberry Pi OS (Legacy 32-bit) Lite
It is Debian Bullseye with no Desktop environment
This means reduced filesize for small board such as Raspi Zero

### LAN Connection:
Configured for Ethan's home internet
Once it connects to internet

Information:
Hostname: raspberrypisd
Username: seniordesign
Password: design

Connect with:
ssh seniordesign@raspberrypisd
enter password and connect

### Progress Made:
#### Commands run:

##### Python 3 & pip

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
pip3 install --upgrade pip
pip3 install numpy

##### Git
sudo apt update
sudo apy install git 

(check to confirm)
sudo mkdir /repo
cd /
I could see the repo so I knew it worked.

##### ML Models downloaded
mkdir tLite
git clone https://github.com/tensorflow/examples -- depth 1
^Above command makes a clone of tensorflow's machine learning models
We can then cd all the way into lite, raspberry_pi, examples, and find all the available models.

Once finding a model such as object detection, we can cd into it and run:
sh setup.sh

Currently having an issue running this setup due to version control

### Issues thus far
#### Power setup
We first needed to power the device, we looked to use the rechargable battery, but after speaking with Raven the TA, no one felt comfortable enough to attempt to recharge it with a power supply.
We also looked at raspberry pi power supplies for the wall. However, these are an added cost and have a long shipping time that did not fit our schedule.
We decided to plug the Raspi into a computer through the microusb power supply port on the board. This works as the board needs between 2.5V and 5V. Which the computer's usb port fits.

#### OS Image on board
We needed to find an OS image that works. We first attempted Raspberry Pi OS (32-bit) without desktop environment.
However, the version we downloaded was the Bookworm version. 
Upon doing work with this version, we found that it did not fit our needs, most tutorials online recommend the Bullseye version.
We had to remove and redownload the Bullseye version (32-bit) without desktop environment.
This meant we had to redo everything thus far.

#### Connecting to the board
We originally had some issues with connecting to the board. When we attempted it in the lab room, we found we would not be able to set the OS to make a connection on eduroam.
We realized we would need a router to work with while on campus, however, I believe we would need an ethernet cable for this, which the board does not have.
We attempted to use a hotspot but found that we had trouble finding the raspberry pi on the hotspot network.

I was able to find it on my home wifi and connect to it. This was done in powershell, but I will probably set up ssh with vscode in the future.

#### Version control CURRENT ISSUE!
The issue we currently face is making sure the versions of everything are correct. When I attempt to run the setup for the object detection model, errors are thrown due to incorrect versions.
The core issue is tflite version, which is tensorflow-lites system and interpreter, which would actually run the model. 
The version that all online tutorials recommend is 0.4.3, otherwise an error would be thrown.
This is supposed to be fixed by running:

python -m pip install --upgrade tflite-support==0.4.3

However, upon running then, another error is thrown saying that the version cannot be found. Error:
ERROR: Could not find a version that satisfies the requirement tflite-support==0.4.3 (from versions: 0.1.0a0.dev3, 0.1.0a0.dev4, 0.1.0a0.dev5, 0.1.0a0, 0.1.0a1)
ERROR: No matching distribution found for tflite-support==0.4.3

I am worried that this tflite version may not be supported by the 32-bit version, as the videos I am watching are using 64 bit.
I do not believe the small Raspberry Pi Zero supports a 64 bit OS. 

I will need to do more research. 