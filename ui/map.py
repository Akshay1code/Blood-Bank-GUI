from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

geolocator = Nominatim(user_agent="blood_bank_app")

location_text = "Dombivli East, Maharashtra"

try:
    location = geolocator.geocode(location_text, timeout=10)

    if location:
        print("Location found")
        print("Latitude:", location.latitude)
        print("Longitude:", location.longitude)
        print("Address:", location.address)
    else:
        print("Location not found. Try a more specific area.")

except GeocoderTimedOut:
    print("⏳ Geocoding timed out. Please try again.")

except GeocoderServiceError as e:
    print("⚠️ Geocoding service error:", e)

except Exception as e:
    print("❌ Unexpected error:", e)
