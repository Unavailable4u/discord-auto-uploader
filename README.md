# Discord Auto Uploader

An automated Python tool that **bypasses Discord's 10 media files per upload limit** by uploading entire folders of images and videos in batches.

## Overview

Discord only allows a maximum of **10 files** to be uploaded at once.  
This script automates the entire process — just put all your media in one folder, run the script, and it will upload everything automatically batch by batch.

## Features

- Uploads hundreds or thousands of photos/videos automatically
- Respects Discord's 10-file upload limit
- Multiple sorting options (Name, Date Modified, Size — Ascending/Descending)
- Configurable batch size and delay between uploads
- Clean progress tracking

## Requirements

- **Python 3.8 or higher** (Must be installed)
- Google Chrome Browser
- Stable internet connection

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Unavailable4u/discord-auto-uploader.git

```
2. Go into the project folder:
```bash
cd discord-auto-uploader
```
3. Install required packages:
```bash
pip install -r requirements.txt
```
4. Run the script:
```bash
python discord_auto_uploader.py
```
## How to Use

1. Put all your images and videos in one folder
2. Run the script
3. Select the folder and choose your sorting preference
4. In the opened Chrome browser:
   - Login to Discord
   - Go to your target channel
   - Click once inside the message input box

Press Enter to start auto-uploading

## Configuration
You can customize these at the top of discord_auto_uploader.py:
```bash
BATCH_SIZE = 10
DELAY_BETWEEN_BATCHES = 7
CUSTOM_MESSAGE = ""        # Add text to send with each batch (optional)
```
## Important Notes

- Use this tool responsibly. Excessive automated uploading may trigger Discord rate limits.
- Keep the browser window open and maximized during the process.
- Works best with a stable internet connection.

## Disclaimer
This project is for educational and personal use only. The author is not responsible for any account restrictions caused by using automation tools on Discord.
## License
MIT License
