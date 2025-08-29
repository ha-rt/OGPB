# Oliver's General Purpose Bot (OGPB)

A general purpose bot which hopes to encompass as many features as possible.

## Building & Running

Clone the repository
```
git clone https://github.com/ha-rt/OGPB
cd OGPB
```

Create a python virtual environment
```
python -m venv venv
# In cmd.exe
venv\Scripts\activate.bat
# In PowerShell
venv\Scripts\Activate.ps1
# In Linux or MacOS
source venv\bin\activate
```
Credit to [python.land](https://python.land/virtual-environments/virtualenv) for the above commands

Create a .env file in the cloned repository with a BOT_TOKEN key

Run the main file
```
python src/main.py
```