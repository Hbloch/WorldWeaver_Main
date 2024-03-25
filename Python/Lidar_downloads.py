import requests
import os
import logging
import pathlib
import math
from requests.exceptions import HTTPError, ConnectionError
from alive_progress import alive_bar
from colorama import Fore, Style, init
from geopy.distance import geodesic


# Initialize Colorama
init()

# Configure logging
logging.basicConfig(level=logging.INFO)

class InputHandler:
    def get_coordinates():
        while True:
            try:
                lat = float(input("Enter the latitude (e.g., 45.35): "))
                lon = float(input("Enter the longitude (e.g., -74.14): "))
                radius = float(input("Enter the radius in meters (max 25000): "))

                if radius > 25000:
                    logging.error(Fore.YELLOW + "Radius exceeds maximum limit of 5000m. Please try again." + Style.RESET_ALL)
                    continue

                # Calculate new coordinates based on radius
                original_point = (lat, lon)
                south = geodesic(meters=radius).destination(original_point, 180).latitude
                north = geodesic(meters=radius).destination(original_point, 0).latitude
                west = geodesic(meters=radius).destination(original_point, 270).longitude
                east = geodesic(meters=radius).destination(original_point, 90).longitude
                print(f"South: {south}, North: {north}, West: {west}, East: {east}")


                return south, north, west, east

            except ValueError:
                logging.error(Fore.YELLOW + "Invalid input. Please enter numerical values for coordinates and radius." + Style.RESET_ALL)

    def get_download_path():
        download_folder = "ImagesDownloads"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        return download_folder

class NASADEMDownloader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://portal.opentopography.org/API/usgsdem"
    
    def download_nasadem(self, south, north, west, east, output_file):
        params = {
            "datasetName": "USGS10m",
            "south": south,
            "north": north,
            "west": west,
            "east": east,
            "outputFormat": "GTiff",
            "API_Key": self.api_key
        }

        try:
            response = requests.get(self.url, params=params, stream=True)
            response.raise_for_status()

            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte

            with open(output_file, "wb") as file, alive_bar(total_size_in_bytes // block_size, title="Downloading") as bar:
                for data in response.iter_content(block_size):
                    bar()
                    file.write(data)
            logging.info(Fore.GREEN + "Download successful." + Style.RESET_ALL)

        except HTTPError as http_err:
            logging.error(Fore.RED + f"HTTP error occurred: {http_err}" + Style.RESET_ALL)
        except ConnectionError as conn_err:
            logging.error(Fore.RED + f"Connection error occurred: {conn_err}" + Style.RESET_ALL)
        except Exception as err:
            logging.error(Fore.RED + f"An error occurred: {err}" + Style.RESET_ALL)
  
    def check_and_rename_file(file_path):
        path = pathlib.Path(file_path)
        if not path.exists():
            return file_path

        # Ask user if they want to overwrite the existing file
        overwrite = input(f"Your old HeightMap still here. Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite == 'yes':
            return file_path

        # File renaming logic if not overwriting
        base_name = path.stem
        extension = path.suffix
        directory = path.parent
        counter = 1

        new_path = directory / f"{base_name}_{counter}{extension}"
        while new_path.exists():
            counter += 1
            new_path = directory / f"{base_name}_{counter}{extension}"

        return str(new_path)

def main():
    print(Fore.RED + "Documentation for this tool can be found at (CTRL + CLICK ON IT):" + Style.RESET_ALL)
    print(Fore.CYAN + "https://docs.google.com/document/d/1qWj2HfVw1_gx8RPa3mEVxtNALCTz-gXi_4xudBaGZUs/edit?usp=sharing" + Style.RESET_ALL)

    api_key = os.getenv('OpentopoAPI')
    if not api_key:
        logging.error(Fore.RED + "No API key found. Set the OpentopoAPI environment variable." + Style.RESET_ALL)
        return

    south, north, west, east = InputHandler.get_coordinates()
    output_path = InputHandler.get_download_path()

    if output_path:
        output_file = os.path.join(output_path, "Topology.tif")
    
    else:  
        output_file = NASADEMDownloader.check_and_rename_file(output_file)

    output_file = NASADEMDownloader.check_and_rename_file(output_file)

    print(Fore.BLUE + "Contacting servers to download data. This may take some time, please be patient." + Style.RESET_ALL)

    downloader = NASADEMDownloader(api_key)
    downloader.download_nasadem(south, north, west, east, output_file)

    print(Fore.GREEN + f"Download completed. File saved at: {os.path.abspath(output_file)}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
