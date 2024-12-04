import requests
import json

# Constants for API endpoints
BASE_URL = "https://panelharga.badanpangan.go.id/data"
PROVINCE_URL = f"{BASE_URL}/provinsi-by-levelharga/1/{{date_from}}/{{date_to}}"
CITY_URL = f"{BASE_URL}/kabkota-by-levelharga/3/{{province_id}}/{{date_from}}/{{date_to}}"
PRICE_URL = f"{BASE_URL}/provinsi-range-by-levelharga/{{province_id}}/3/{{date_from}}/{{date_to}}"

# Date range in dd-mm-yyyy format
DATE_FROM = "22-11-2024"
DATE_TO = "29-11-2024"

# Commodity name
COMMODITY = "Bawang Merah"

def fetch_provinces():
    """Fetches the list of provinces."""
    try:
        url = PROVINCE_URL.format(date_from=DATE_FROM, date_to=DATE_TO)
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching provinces: {e}")
        return []

def fetch_cities(province_id):
    """Fetches the list of cities for a given province."""
    try:
        url = CITY_URL.format(province_id=province_id, date_from=DATE_FROM, date_to=DATE_TO)
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching cities for province_id {province_id}: {e}")
        return []

def fetch_prices(province_id, city_id):
    """Fetches the prices for a given province and city."""
    try:
        url = PRICE_URL.format(province_id=province_id, city_id=city_id, date_from=DATE_FROM, date_to=DATE_TO)
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching prices for province_id {province_id}, city_id {city_id}: {e}")
        return []

def main():
    # Initialize result structure
    result = {"commodity": COMMODITY, "prices": []}

    # Fetch provinces
    provinces = fetch_provinces()
    if not provinces:
        print("No provinces found. Exiting.")
        return

    for province in provinces:
        province_id = province.get("id")
        province_name = province.get("nama", "Unknown Province")

        # Fetch cities in the province
        cities = fetch_cities(province_id)
        if not cities:
            print(f"No cities found for province_id {province_id}. Skipping.")
            continue

        for city in cities:
            city_id = city.get("id")
            city_name = city.get("nama", "Unknown City")

            # Fetch prices for the city
            prices = fetch_prices(province_id, city_id)
            if not prices:
                print(f"No prices found for province_id {province_id}, city_id {city_id}. Skipping.")
                continue

            for price_entry in prices:
                # Add price data to the result
                for by_date in price_entry.get("by_date", []):
                    result["prices"].append({
                        "province_id": province_id,
                        "province": province_name,
                        "city_id": city_id,
                        "city": city_name,
                        "commodity_name": price_entry.get("name", "Unknown Commodity"),
                        "date": by_date.get("date", "Unknown Date"),
                        "avg_price": by_date.get("geomean", 0)
                    })

    # Save to JSON file
    output_file = "commodity_prices.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
