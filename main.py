from typing import List
import requests
import sys
import io
import os
import time
import ctypes

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def fetch_image_urls(subreddit_url: str) -> List[str]:
    """Fetch image URLs from a subreddit JSON feed."""
    response = requests.get(subreddit_url, headers={"User-agent": "your bot 0.1"})
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    data = response.json()
    return [
        post["data"].get("url")
        for post in data["data"]["children"]
        if post["data"].get("url", "").endswith((".jpg", ".png"))
    ]

def download_images(image_urls: List[str], download_dir: str) -> None:
    """Download images from the list of URLs and save them to the specified directory."""
    os.makedirs(download_dir, exist_ok=True)
    for image_url in image_urls:
        try:
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_name = os.path.basename(image_url)
                image_path = os.path.join(download_dir, image_name)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_response.content)
                print(f"Downloaded: {image_url}")
            else:
                print(f"Failed to download image: {image_url}")
        except requests.RequestException as e:
            print(f"Error downloading {image_url}: {e}")

def set_wallpaper(image_path: str) -> None:
    """Set the desktop wallpaper to the specified image path."""
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

def cycle_wallpapers(download_dir: str, interval: int = 3600) -> None:
    """Cycle through downloaded images and set them as wallpaper at specified intervals."""
    image_files = [
        f for f in os.listdir(download_dir) if f.endswith((".jpg", ".png"))
    ]
    while True:
        for image_file in image_files:
            image_path = os.path.join(download_dir, image_file)
            set_wallpaper(image_path)
            print(f"Wallpaper set to: {image_file}")
            time.sleep(interval)

def main():
    subreddit_url = "https://www.reddit.com/r/EarthPorn/.json"
    download_dir = "downloaded_images"
    image_urls = fetch_image_urls(subreddit_url)
    download_images(image_urls, download_dir)
    cycle_wallpapers(download_dir)

if __name__ == "__main__":
    main()
