import asyncio

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_travel_bot")

async def get_city_by_coordinates(lat, lng, lang):
    location = geolocator.reverse(f"{lat}, {lng}", language=lang)

    if location is None:
        return None

    address = location.raw.get("address")
    if not address:
        return None

    city = address.get("city") or address.get("town") or address.get("village")
    return city

async def get_city_by_address(address, lang):
    try:
        location = await asyncio.to_thread(
            geolocator.geocode,
            address,
            language=lang,
            featuretype = "settlement",
            addressdetails = True
        )
        if location:
            address_data = location.raw.get("address", {})
            city = (
                    address_data.get("city") or
                    address_data.get("town") or
                    address_data.get("village") or
                    address_data.get("hamlet") or
                    address_data.get("state")
            )
            return city if city else False

        return False
    except Exception as e:
        print(f"Error geocoding: {e}")
        return False
