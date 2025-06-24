import geocoder

def detect_location():
    try:
        g = geocoder.ip("me")
        return g.city
    except:
        return None
