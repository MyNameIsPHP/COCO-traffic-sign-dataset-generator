import os
import cv2
import numpy as np
import random

def generate_random_lines(imshape, slant_range, drop_length):
    drops = []
    for i in range(1500):  # If you want heavy rain, try increasing this
        slant = np.random.randint(-slant_range, slant_range)
        if slant < 0:
            x = np.random.randint(slant, imshape[1])
        else:
            x = np.random.randint(0, imshape[1] - slant)
            y = np.random.randint(0, imshape[0] - drop_length)
            drops.append((x, y, slant))
    return drops


def add_rain(image, drop_length):
    try:
        imshape = image.shape
        slant = 5  # Set a fixed value for slant (you can adjust this value)
        drop_width = 1
        drop_color = (200, 200, 200)  # a shade of gray
        rain_drops = generate_random_lines(imshape, slant, drop_length)
        for rain_drop in rain_drops:
            cv2.line(image, (rain_drop[0], rain_drop[1]), (rain_drop[0] + slant, rain_drop[1] + drop_length), drop_color, drop_width)
        brightness_coefficient = 0.7  # rainy days are usually shady
        image_HLS = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)  # Conversion to HLS
        image_HLS[:, :, 1] = image_HLS[:, :, 1] * brightness_coefficient  # scale pixel values down for channel 1 (Lightness)
        image_RGB = cv2.cvtColor(image_HLS, cv2.COLOR_HLS2RGB)  # Conversion to RGB
        return image_RGB
    except Exception as e:
        print(f"Error in image processing: {e}")
        return None