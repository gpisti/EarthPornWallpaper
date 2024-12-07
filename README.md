# Reddit Image Downloader and Wallpaper Cycler

This Python script fetches image URLs from a specified subreddit, downloads the images, and cycles them as desktop wallpapers at a specified interval.

## Features

- Fetches image URLs from a subreddit JSON feed.
- Downloads images to a specified directory.
- Sets downloaded images as desktop wallpapers.
- Cycles through wallpapers at a specified interval.

## Requirements

- Python 3.12 or later
- `requests` library

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages using pip:

   ```bash
   pip install requests
   ```
## Usage
1. Open the script and modify the `subreddit_url` variable in the `main()` function to point to your desired subreddit JSON feed.
2. Run the script:
```bash
python main.py
```
3. The script will download images to the `downloaded_images` directory and cycle them as wallpapers.

## Configuration
- ***Subreddit URL***: Change the `subreddit_url` variable in the `main()` function to fetch images from a different subreddit.
- ***Download Directory***: Change the `download_dir` variable in the `main()` function to specify a different directory for downloaded images.
- ***Wallpaper Interval***: Adjust the `interval` parameter in the `cycle_wallpapers()` function to change the time between wallpaper changes (default is 3600 seconds).
## Notes
- Ensure that the script has permission to change the desktop wallpaper on your system.
- The script is designed for Windows systems due to the use of `ctypes` for setting wallpapers.
