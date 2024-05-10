import unreal
import os
import requests
from geopy.distance import geodesic
from pathlib import Path

def log_message(message, severity='info'):
    if severity == 'info':
        unreal.log(message)
    elif severity == 'error':
        unreal.log_error(message)
    elif severity == 'warning':
        unreal.log_warning(message)

def validate_coordinates(lat, lon):
    """Check if the coordinates are valid."""
    return -90 <= lat <= 90 and -180 <= lon <= 180

def calculate_square_bounds(lat, lon, area_km2):
    """Calculate the bounds for a square of the specified area around the given coordinates."""
    side_length_m = (area_km2 ** 0.5) * 1000  # Convert to meters
    original_point = (lat, lon)
    half_side_m = side_length_m / 2
    south = geodesic(meters=half_side_m).destination(original_point, 180).latitude
    north = geodesic(meters=half_side_m).destination(original_point, 0).latitude
    west = geodesic(meters=half_side_m).destination(original_point, 270).longitude
    east = geodesic(meters=half_side_m).destination(original_point, 90).longitude
    return south, north, west, east

def get_download_path():
    """Get or create the download folder."""
    download_folder = Path(unreal.Paths.project_content_dir()) / "DownloadedImages"
    download_folder.mkdir(parents=True, exist_ok=True)
    return download_folder


class DataDownloader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://portal.opentopography.org/API/usgsdem"

    def download_data(self, south, north, west, east, output_file):
        params = {
            "datasetName": "USGS1m",
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
            with open(output_file, "wb") as file:
                for data in response.iter_content(16384):
                    file.write(data)
            log_message("Download successful.")
            return False
        except Exception as e:
            log_message(f"An error occurred during the download: {str(e)}", severity='error')
            return True
        
def import_to_unreal(file_path, destination_path):
    """Import the downloaded file to Unreal Engine."""
    task = unreal.AssetImportTask()
    task.filename = file_path
    task.destination_path = destination_path
    task.automated = True

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])



def main():
    lat, lon = 44.589830, -104.713372 # Example coordinates for Los Angeles
    area_km2 = 2  # Area in square kilometers
    api_key = "ee8c4f4ac91d78b34c0baf3049e5fe4d"

    if not api_key:
        log_message("API key missing.", severity='error')
        return

    if not validate_coordinates(lat, lon):
        log_message("Invalid coordinates.", severity='error')
        return

    coordinates = calculate_square_bounds(lat, lon, area_km2)
    output_path = get_download_path()
    output_file = output_path / "Topography.tif"

    downloader = DataDownloader(api_key)
    error_occurred = downloader.download_data(*coordinates, str(output_file))

    if error_occurred:
        log_message("Do you want to check the log file for errors?", severity='warning')
    else:
        log_message(f"Download completed. File saved at: {output_file.resolve()}")
        import_to_unreal(str(output_file.resolve()), "/Game/DownloadedImages")
        
main()
