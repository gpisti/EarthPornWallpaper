from typing import List, Union
import json
import os
import requests
import ctypes
import time


def find_image_urls(data: Union[dict, list]) -> List[str]:
    """
    Recursively find and return a list of unique image URLs from the given data.

    The function searches for URLs in dictionaries with keys "url" or
    "url_overridden_by_dest" that contain "i.redd.it". It processes both
    dictionaries and lists, handling nested structures.

    Args:
        data (Union[dict, list]): The data structure to search for image URLs.

    Returns:
        List[str]: A list of unique image URLs found in the data.
    """
    image_urls = set()

    if isinstance(data, dict):
        for key, value in data.items():
            if key in {"url", "url_overridden_by_dest"} and "i.redd.it" in value:
                image_urls.add(value)
            elif isinstance(value, (dict, list)):
                image_urls.update(find_image_urls(value))
    elif isinstance(data, list):
        for item in data:
            image_urls.update(find_image_urls(item))

    return list(image_urls)


def download_image(url: str, download_folder: str) -> Union[str, None]:
    """
    Download an image from a given URL and save it to the specified folder.

    Args:
        url (str): The URL of the image to download.
        download_folder (str): The folder where the image will be saved.

    Returns:
        Union[str, None]: The file path of the downloaded image if successful,
        otherwise None.
    """
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(download_folder, os.path.basename(url))
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    return None


def set_wallpaper(image_path: str) -> None:
    """
    Set the desktop wallpaper to the specified image.

    Args:
        image_path (str): The file path to the image to be set as wallpaper.

    Returns:
        None
    """
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)


def main() -> None:
    """
    Main function to load image data from a JSON file, download images,
    and set them as wallpapers in a loop.

    This function reads image data from 'reddit.json', extracts image URLs,
    downloads the images to a specified folder, and sets them as wallpapers
    in a continuous loop with a delay.
    """
    with open("reddit.json", "r") as file:
        data = json.load(file)

    urls = find_image_urls(data)
    download_folder = "downloaded_images"
    os.makedirs(download_folder, exist_ok=True)

    while True:
        for url in urls:
            image_path = download_image(url, download_folder)
            if image_path:
                set_wallpaper(image_path)
                time.sleep(1)


if __name__ == "__main__":
    main()
