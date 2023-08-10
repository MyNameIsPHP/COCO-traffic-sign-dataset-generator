
import os
from PIL import Image, ImageEnhance
import random

def apply_sunny_effect(image, brightness_factor=1.2, contrast_factor=1.2, tint_color=(255, 255, 150)):
    """
    Apply a sunny effect to the input PIL image.

    Parameters:
    image (PIL.Image): The input image.
    brightness_factor (float): Controls the brightness enhancement. Default is 1.2.
    contrast_factor (float): Controls the contrast enhancement. Default is 1.2.
    tint_color (tuple): The color used to add a yellow tint to the image. Default is (255, 255, 150).

    Returns:
    PIL.Image: The image with the sunny effect applied.
    """
    # Apply brightness enhancement
    enhancer = ImageEnhance.Brightness(image)
    enhanced_image = enhancer.enhance(brightness_factor)

    # Apply contrast enhancement
    enhancer = ImageEnhance.Contrast(enhanced_image)
    enhanced_image = enhancer.enhance(contrast_factor)

    # Add yellow tint to the image
    tint_layer = Image.new("RGB", image.size, tint_color).convert('RGBA')
    tinted_image = Image.blend(enhanced_image, tint_layer, random.uniform(0.1, 0.3))

    return tinted_image

