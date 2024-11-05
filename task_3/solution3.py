import numpy as np


def transform_time_to_cyclic_features(hour):
    if hour < 0 or hour >= 24:
        raise ValueError("Hour must be between 0 and 24.")
    
    radians = (hour / 24) * (2 * np.pi)  # Convert hour to radians. Transform hour (0-24) into cyclic features using sine and cosine
    return np.cos(radians), np.sin(radians)

def calculate_cyclic_time_difference(start_hour, end_hour):
    if start_hour < 0 or start_hour >= 24 or end_hour < 0 or end_hour >= 24:
        raise ValueError("Hours must be between 0 and 24.")
    
    difference = end_hour - start_hour
    if difference < 0:
        difference += 24  # Wrap around if negative
    
    return difference
