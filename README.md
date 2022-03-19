# Robotics ROBber Hand

## Description
Robotic version of the rubber hand experiement. A webacm capture the position of the finger tips (with color markers) and send the angle to the device. The device is composed of four servo motors driven by a PCA9685 driver and an arduino uno. A fake hand is placed on top of the device and each finger is pushed up by the device.

![CAD](/img/P1.PNG)

### List of material
- 4 servos motors MG90(metal gear) or SG90 (plastic gears)
- 1 servo driver PCA9685
- 1 arduino
- Screws and Bolts:
  - 8 M3-12mm
  - 4 M3-16mm
  - 12 M5-20mm
  - 4 M5 bolt

### Parts to print
- 1 ![frame](/models/frame.stl)
- 1 ![lid](/models/frame.stl)
- 4 ![foot](/models/frame.stl)
- 1 ![arduinoUNO and PCA holder](/models/arduinoUNO_PCA_holder.stl)
- 2 ![p1_short](/models/p1_short.stl)
- 2 ![p1_long](/models/p1_long.stl)
- 4 ![p2](/models/p2.stl)
- 2 ![p3_short](/models/p3_short.stl)
- 2 ![p3_long](/models/p3_long.stl)
- 2 ![p4_short](/models/p4_short.stl)
- 2 ![p4_long](/models/p4_long.stl)
- 4 ![bolt](/models/bolt.stl)

## Requirements
- Python3/pip installed.

## Installation
### Electronics
![CAD](/img/elec.png)

### Firmware
- Plug the arduino to the computer.
- Open the arduino IDE
- Ensure you have the last verdion of the library **Adafruit PWM Servo Driver** (go to the menu _sketch>Include library>Libraries Manager_ and search for "PWM".
- Open the file scripts/arduino.ide of the repository
- Upload it on the arduino board. 


### Software
- Download the zip folder at https://github.com/Aightech/ROBber_hand .
- Extract it
- Open the folder.
- Open the folder named **scripts**
- While pressing the **shift key** right click in the folder and select the option **open PowerShell**

Inside the PowerShell terminal:
- Install required libraries by entering the following command in the PowerShell terminal.
```bash 
pip install -r requirements.txt
```
## Usage

### Setup
- Plug the arduino USB wire to the computer.
- Plug the Webcam to the computer.
- Connect the motor driver to a power supply (ex: a phone charger).

### Setting:
To ensure the different parameters of the experiments are correct run the program setting with the command:
```bash 
python setting.py <NB_CAM> 
```
Replace :
- **<NB_CAM>** by the number of the webcam (usually 1 for laptop with integrated cam, else 0).

### Experiment
To launch the experiment use the command:
```bash 
python run.py <ARDUINO_PORT> <NB_CAM>
```
Replace :
- **<ARDUINO_PORT>** by the port used by the arduino (usually COM3, COM4, ...).
- **<NB_CAM>** by the number of the webcam (usually 1 for laptop with integrated cam, else 0).

### Options

in the script named **scripts/run.py** you can modify the following lines to modify the behavior of the robot.
```python
# BUFFER SIZE AND LOOKUP TABLE
lookup_table = [0, 1, 2, 3] # [nb finger cmd] => nb finger controlled
BUFF_SIZE = 1 # Delay of the control (no unit... depends of you communication speed)
inverted_finger = False  # When human finger up => robot finger down 
```

# Debug

In a terminal you can use the script **sendCmd.sh** to send position order to the Robber hand. Here an exemple:
```bash
Usage: scripts/sendCmd.sh [pos1] [pos2] [pos3] [pos4] port
Ex: scripts/sendCmd.sh 20 40 50 60 /dev/ttyUSB0
```
