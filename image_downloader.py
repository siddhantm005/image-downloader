from pathlib import Path
import requests

from exceptions import ImageDownloadError


def get_image(url: str, image_file_path: str) -> bool:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(image_file_path, 'wb') as output_file:
            for chunk in response.iter_content(chunk_size=8192):
                output_file.write(chunk)

        return True
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to download: {url}\nError: {e}"
        raise ImageDownloadError(error_msg) from e
    except IOError as e:
        error_msg = f"Failed to save: {image_file_path}\nError: {e}"
        raise ImageDownloadError(error_msg) from e


def download_images_from_file(text_file_path: str, output_folder_name: str):
    output_file_path = Path(output_folder_name)
    output_file_path.mkdir(parents=True, exist_ok=True)

    with open(text_file_path, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            file_name = url.rsplit("/", maxsplit=1)[-1]
            image_file_path = output_file_path / file_name
            try:
                if get_image(url, str(image_file_path)):
                    print(f"Image Downloaded: {file_name}")
            except ImageDownloadError as e:
                print(str(e))
