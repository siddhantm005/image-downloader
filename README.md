# image-downloader
Image Downloader is a script that downloads images from a list of URLs provided in a plaintext file. It utilizes the requests library to perform the image downloads and saves them to a specified directory on the local hard disk.

# Installation
* Clone the repository or download the script file.
* Make sure Python 3 is installed on your system.

# Usage
* Prepare a plaintext file containing the URLs of the images that needs to be downloaded. Each URL should be on a separate line.
* Open a terminal and navigate to the directory where the script is located.
* Run the script with the following command:
```Python
python image_downloader.py <file_path> <output_directory>
```
Replace `<file_path>` with the path to the plaintext file containing the URLs, and `<output_directory>` with the directory where you want to save the downloaded images.

* The script will download the images one by one and save them to the specified output directory.
* After the script finishes, the downloaded images can be found in the specified output directory.

# Error Handling
If any errors occur during the image download or file saving process, an `ImageDownloadError` will be raised with the corresponding error message. The script will print the error message to the console.

# Dependencies
The script relies on the following dependencies:
* Python3
* requests library

The required dependencies can be installed by running the following command:
```Python
pip install requests
```