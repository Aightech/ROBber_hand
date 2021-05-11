# Robotics ROBber Hand

## Descriptiom
![CAD](/img/P1.PNG)

## Requirements
- Python installed.

## Installation

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
