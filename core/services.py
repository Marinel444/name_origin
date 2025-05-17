import requests


def get_nationalize_data(name: str):
    url = f"https://api.nationalize.io/?name={name}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


def get_country_data(code: str):
    url = f"https://restcountries.com/v3.1/alpha/{code}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()[0]
    capital_coords = data.get("capitalInfo", {}).get("latlng", [None, None])
    flags = data.get("flags", {})
    coat = data.get("coatOfArms", {})

    return {
        "code": data.get("cca2"),
        "name": data["name"].get("common"),
        "official_name": data["name"].get("official"),
        "region": data.get("region"),
        "subregion": data.get("subregion"),
        "independent": data.get("independent"),
        "google_maps": data.get("maps", {}).get("googleMaps"),
        "openstreetmap": data.get("maps", {}).get("openStreetMaps"),
        "capital_name": data.get("capital", [None])[0],
        "capital_lat": capital_coords[0],
        "capital_lng": capital_coords[1],
        "flag_png": flags.get("png"),
        "flag_svg": flags.get("svg"),
        "flag_alt": flags.get("alt"),
        "coat_png": coat.get("png"),
        "coat_svg": coat.get("svg"),
        "borders": data.get("borders", []),
    }
