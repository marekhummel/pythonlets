import phonenumbers as pn
from phonenumbers import carrier, geocoder, timezone

mobile_no_str = "+12339123123"
culture = "en"

mobile_no = pn.parse(mobile_no_str)

print(timezone.time_zones_for_number(mobile_no))
print(carrier.name_for_number(mobile_no, culture))
print(geocoder.description_for_number(mobile_no, culture))
print(f"Valid: {pn.is_valid_number(mobile_no)}")
print(f"Possible: {pn.is_possible_number(mobile_no)}")
