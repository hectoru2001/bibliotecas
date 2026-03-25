# utils.py
import requests
from django.conf import settings
from math import radians, sin, cos, sqrt, atan2

class GrokChatbot:
    def __init__(self):
        self.api_key = settings.XAI_API_KEY
        self.api_url = "https://api.xai.com/v1/grok" 

    def get_response(self, user_input):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "prompt": user_input,
            "max_tokens": 150,
            "model": "grok",  
        }
        try:
            response = requests.post(self.api_url, json=data, headers=headers)
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            return response.json().get("response", "No pude procesar tu solicitud.")
        except requests.exceptions.RequestException as e:
            return f"Error al conectar con la API de xAI: {str(e)}"

def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate the distance between two points on Earth using the Haversine formula."""
        # Radius of the Earth in kilometers
        R = 6371.0

        # Convert latitude and longitude to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Differences in coordinates
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        return distance  # Distance in kilometersn la API de xAI: {str(e)}"