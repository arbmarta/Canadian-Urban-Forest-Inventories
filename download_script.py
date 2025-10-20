import requests
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from inventories import Inventories
from tqdm import tqdm


class DownloadStats:
    """Track download statistics and errors"""

    def __init__(self):
        self.successful = []
        self.empty_records = []
        self.api_errors = []

    def add_success(self, city, records):
        if records == 0:
            self.empty_records.append(city)
        else:
            self.successful.append({'city': city, 'records': records})

    def add_api_error(self, city, error):
        self.api_errors.append({'city': city, 'error': error})

    def print_summary(self):
        print("\n" + "=" * 70)
        print("DOWNLOAD SUMMARY")
        print("=" * 70)

        if self.successful:
            print(f"\n✓ Successfully downloaded: {len(self.successful)} cities")
            for item in sorted(self.successful, key=lambda x: x['records'], reverse=True):
                print(f"  • {item['city']:<25} {item['records']:>8,} records")

        if self.empty_records:
            print(f"\n⚠ Cities with empty records: {len(self.empty_records)}")
            for city in sorted(self.empty_records):
                print(f"  • {city}")

        if self.api_errors:
            print(f"\n✗ Cities with API errors: {len(self.api_errors)}")
            for item in sorted(self.api_errors, key=lambda x: x['city']):
                print(f"  • {item['city']:<25} {item['error']}")

        print("=" * 70)

        # Return True if there are any issues
        has_issues = len(self.empty_records) > 0 or len(self.api_errors) > 0
        return not has_issues


def download_arcgis_data(base_url, city_name, output_dir, output_format='csv', max_records=None, pbar=None):
    """
    Download data from ArcGIS REST API endpoint.
    Returns: tuple (success: bool, record_count: int, error_message: str or None)
    """

    params = {
        'where': '1=1',
        'outFields': '*',
        'f': 'json',
        'returnGeometry': 'true',
        'outSR': '4326'
    }

    all_features = []
    offset = 0
    batch_size = 1000

    try:
        while True:
            params['resultOffset'] = offset
            params['resultRecordCount'] = batch_size

            try:
                response = requests.get(base_url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                if 'error' in data:
                    error_msg = f"{data['error'].get('message', 'Unknown API error')}"
                    if pbar:
                        pbar.set_postfix_str(f"API Error")
                    return False, 0, error_msg

                features = data.get('features', [])

                if not features:
                    break

                all_features.extend(features)

                # Update progress bar with current count
                if pbar:
                    pbar.set_postfix_str(f"{len(all_features):,} records")

                if max_records and len(all_features) >= max_records:
                    all_features = all_features[:max_records]
                    break

                if len(features) < batch_size:
                    break

                offset += batch_size

            except requests.exceptions.Timeout:
                error_msg = "Request timeout"
                if pbar:
                    pbar.set_postfix_str("Timeout")
                return False, len(all_features), error_msg
            except requests.exceptions.RequestException as e:
                error_msg = f"Request failed: {type(e).__name__}"
                if pbar:
                    pbar.set_postfix_str("Failed")
                return False, len(all_features), error_msg

        # Save the data
        date_str = datetime.now().strftime('%Y%m%d')

        if output_format == 'csv':
            records = []
            for feature in all_features:
                record = feature.get('attributes', {})
                if 'geometry' in feature:
                    geom = feature['geometry']
                    if 'x' in geom and 'y' in geom:
                        record['longitude'] = geom['x']
                        record['latitude'] = geom['y']
                records.append(record)

            if records:
                df = pd.DataFrame(records)
                filename = output_dir / f'{city_name}_{date_str}.csv'
                df.to_csv(filename, index=False, encoding='utf-8')

                if not filename.exists() or filename.stat().st_size == 0:
                    error_msg = "File creation failed"
                    return False, len(all_features), error_msg

        if pbar:
            pbar.set_postfix_str(f"✓ {len(all_features):,} records")

        return True, len(all_features), None

    except Exception as e:
        error_msg = f"Unexpected error: {type(e).__name__}"
        if pbar:
            pbar.set_postfix_str("Error")
        return False, 0, error_msg


def download_all_inventories(output_format='csv', max_records=None):
    """
    Download data from all cities in the Inventories class.
    Returns: bool indicating if all downloads were successful
    """
    date_str = datetime.now().strftime('%Y%m%d')
    output_dir = Path(date_str)
    output_dir.mkdir(exist_ok=True)

    print(f"📁 Output directory: {output_dir}\n")

    stats = DownloadStats()

    # Count total cities
    total_cities = sum(len(cities) for cities in Inventories.data.values())

    # Create progress bar
    with tqdm(total=total_cities, desc="Downloading", unit="city", ncols=100) as pbar:
        for province, cities in Inventories.data.items():
            for city, url in cities.items():
                pbar.set_description(f"📥 {city:<20}")

                success, record_count, error = download_arcgis_data(
                    url, city, output_dir, output_format, max_records, pbar
                )

                if success:
                    stats.add_success(city, record_count)
                else:
                    if error and ('API Error' in error or 'Invalid query' in error):
                        stats.add_api_error(city, error)
                    else:
                        stats.add_success(city, 0)  # Empty records

                pbar.update(1)

    print(f"\n✓ All downloads complete! Files saved in '{output_dir}' folder.")

    # Print summary and return success status
    all_successful = stats.print_summary()

    if not all_successful:
        raise Exception("Some downloads had issues. Check the summary above for details.")

    return all_successful


if __name__ == '__main__':
    print("=" * 70)
    print("🌲 Canadian Urban Forest Inventories - Monthly Download")
    print("=" * 70)
    print()

    try:
        download_all_inventories(output_format='csv')
        print("\n✓ Download completed successfully!")
    except Exception as e:
        print(f"\n❌ DOWNLOAD COMPLETED WITH ISSUES")
        print(f"   Check the summary above for details.")
        exit(1)