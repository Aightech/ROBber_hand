# Robotics Rubber Hand

## Descriptiom

## Requirements
- Python installed.

## Installation

- Download the zip folder at https://github.com/Aightech/robber_hand .
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
