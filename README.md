# Oliver's General Purpose Bot (OGPB)

A general purpose bot which hopes to encompass as many features as possible.

## Building & Running

### 1. Clone the repository
git clone https://github.com/ha-rt/OGPB  
cd OGPB

### 2. Create a Python virtual environment
python -m venv venv

Activate the virtual environment depending on your system:

- **Windows (Command Prompt)**  
venv\Scripts\activate.bat

- **Windows (PowerShell)**  
venv\Scripts\Activate.ps1

- **Linux / macOS**  
source venv/bin/activate

> Credit: [python.land](https://python.land/virtual-environments/virtualenv)

### 3. Set up your `.env` file
Copy the `.env.template` file to `.env` and add your bot token:

cp .env.template .env

Or manually copy/rename the file. Then edit `.env` to include:

BOT_TOKEN=your_bot_token_here

### 4. Run the bot
python src/main.py
