import requests
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from inventories import Inventories


def download_arcgis_data(base_url, city_name, output_dir, output_format='csv', max_records=None):
    """
    Download data from ArcGIS REST API endpoint.

    Args:
        base_url: The ArcGIS REST service URL
        city_name: Name of the city for file naming
        output_dir: Directory to save the file
        output_format: 'json', 'csv', or 'geojson'
        max_records: Maximum number of records to download (None for all)
    """

    # Parameters for the query
    params = {
        'where': '1=1',  # Get all records
        'outFields': '*',  # Get all fields
        'f': 'json',  # Response format
        'returnGeometry': 'true',
        'outSR': '4326'  # WGS84 coordinate system
    }

    all_features = []
    offset = 0
    batch_size = 1000  # ArcGIS typically has a limit per request

    print(f"Downloading data for {city_name}...")

    while True:
        # Add pagination parameters
        params['resultOffset'] = offset
        params['resultRecordCount'] = batch_size

        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Check for errors
            if 'error' in data:
                print(f"API Error: {data['error']}")
                break

            features = data.get('features', [])

            if not features:
                break

            all_features.extend(features)
            print(f"  {city_name}: Downloaded {len(all_features)} records...")

            # Check if we've reached max_records
            if max_records and len(all_features) >= max_records:
                all_features = all_features[:max_records]
                break

            # Check if there are more records
            if len(features) < batch_size:
                break

            offset += batch_size

        except requests.exceptions.RequestException as e:
            print(f"  {city_name}: Request failed: {e}")
            break

    print(f"  {city_name}: Total records downloaded: {len(all_features)}")

    # Create filename with city and date
    date_str = datetime.now().strftime('%Y%m%d')

    if output_format == 'json':
        filename = output_dir / f'{city_name}_{date_str}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({'features': all_features}, f, indent=2)
        print(f"  Data saved to {filename}")

    elif output_format == 'geojson':
        filename = output_dir / f'{city_name}_{date_str}.geojson'
        geojson = {
            'type': 'FeatureCollection',
            'features': all_features
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, indent=2)
        print(f"  Data saved to {filename}")

    elif output_format == 'csv':
        # Extract attributes into a flat structure
        records = []
        for feature in all_features:
            record = feature.get('attributes', {})
            # Add geometry info if needed
            if 'geometry' in feature:
                geom = feature['geometry']
                if 'x' in geom and 'y' in geom:
                    record['longitude'] = geom['x']
                    record['latitude'] = geom['y']
            records.append(record)

        df = pd.DataFrame(records)
        filename = output_dir / f'{city_name}_{date_str}.csv'
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"  Data saved to {filename}")

    return all_features


def download_all_inventories(output_format='csv', max_records=None):
    """
    Download data from all cities in the Inventories class.

    Args:
        output_format: 'json', 'csv', or 'geojson'
        max_records: Maximum number of records per city (None for all)
    """
    # Create folder named for today's date
    date_str = datetime.now().strftime('%Y%m%d')
    output_dir = Path(date_str)
    output_dir.mkdir(exist_ok=True)

    print(f"Created output directory: {output_dir}\n")

    # Iterate through all provinces and cities
    for province, cities in Inventories.data.items():
        print(f"\n{province}:")
        for city, url in cities.items():
            try:
                download_arcgis_data(url, city, output_dir, output_format, max_records)
            except Exception as e:
                print(f"  {city}: Failed to download - {e}")

    print(f"\n\nAll downloads complete! Files saved in '{output_dir}' folder.")


if __name__ == '__main__':
    # Download all inventories
    download_all_inventories(output_format='csv')

    # Or download just one city:
    # date_str = datetime.now().strftime('%Y%m%d')
    # output_dir = Path(date_str)
    # output_dir.mkdir(exist_ok=True)
    # url = 'https://geoportal.kelowna.ca/arcgis/rest/services/ArcGISOnline/OpenData_Environment/MapServer/17/query'
    # download_arcgis_data(url, 'Kelowna', output_dir, output_format='csv')