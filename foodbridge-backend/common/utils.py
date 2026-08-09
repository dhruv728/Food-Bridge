import random
import string
from common.gis import Point

def generate_otp_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def create_geography_point(latitude, longitude):
    return Point(float(longitude), float(latitude), srid=4326)

def calculate_co2_avoided(kg_food):
    # Standard estimate: 1 kg of food saved avoids ~2.5 kg CO2 equivalent emissions
    return round(float(kg_food) * 2.5, 2)

def calculate_estimated_meals(kg_food):
    # Standard estimate: 1 meal is approximately 0.35 kg (350 grams) of food
    return int(float(kg_food) / 0.35)
