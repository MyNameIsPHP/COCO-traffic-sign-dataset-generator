import math
import random
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import my_transform
import numpy as np

def adjust_brightness(image, brightness_factor):
    """
    Adjust the brightness of the input PIL image.
    The brightness_factor controls the adjustment, where 1.0 is the original image.
    """
    enhancer = ImageEnhance.Brightness(image)
    adjusted_image = enhancer.enhance(brightness_factor)
    return adjusted_image

def adjust_contrast(image, contrast_factor):
    """
    Adjust the contrast of the input PIL image.
    The contrast_factor controls the adjustment, where 1.0 is the original image.
    """
    enhancer = ImageEnhance.Contrast(image)
    adjusted_image = enhancer.enhance(contrast_factor)
    return adjusted_image

def random_rotate(image, min_degree, max_degree):
    """
    Randomly rotate the input PIL image by an angle within the specified range.
    """
    rotation_angle = random.uniform(min_degree, max_degree)
    rotated_image = image.rotate(rotation_angle, resample=Image.BICUBIC, expand=True)
    return rotated_image

def remove_transparent_padding(image):
    # Convert the image to RGBA mode if not already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Get the image data as a list of pixels
    pixels = list(image.getdata())
    
    # Calculate the bounding box of non-transparent pixels
    left, upper, right, lower = image.width, image.height, 0, 0
    for x, y in [(i % image.width, i // image.width) for i in range(len(pixels))]:
        if pixels[x + y * image.width][3] > 0:  # Check alpha value
            left = min(left, x)
            upper = min(upper, y)
            right = max(right, x)
            lower = max(lower, y)
    
    # Crop the image to the bounding box
    cropped_image = image.crop((left, upper, right + 1, lower + 1))
    
    return cropped_image

def apply_occlusion(image, occlusion_size):
    """
    Apply occlusion to the input PIL image.
    The occlusion_size controls the size of the occlusion region, specified as a tuple (width, height).
    """
    width, height = image.size
    occlusion_width, occlusion_height = occlusion_size

    # Generate random occlusion coordinates within the image bounds
    x = random.randint(0, width - occlusion_width)
    y = random.randint(0, height - occlusion_height)

    # Create an occlusion region of the specified size and fill it with a constant color
    occlusion = Image.new('RGB', occlusion_size, (0, 0, 0))
    
    # Paste the occlusion region onto the image at the generated coordinates
    occluded_image = image.copy()
    occluded_image.paste(occlusion, (x, y))

    return occluded_image

def add_transparent_padding(image, padding_size):
    # Get the original image size
    original_width, original_height = image.size

    # Calculate the new image size with padding
    new_width = original_width + 2 * padding_size
    new_height = original_height + 2 * padding_size

    # Create a new transparent image with padding
    padded_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

    # Paste the original image onto the new image with padding
    padded_image.paste(image, (padding_size, padding_size))

    return padded_image

def apply_shear(input_image, padding=100, shear_factor=0.2):
    input_image = add_transparent_padding(input_image, padding)

    # Open the image using Pillow

    # Apply shear effect
    width, height = input_image.size
    shear_matrix = (1, shear_factor, 0, 0, 1, 0)
    sheared_img = input_image.transform((width, height), Image.AFFINE, shear_matrix)

    return sheared_img


def pincushion_distortion(input_image, padding=50, strength=0.1):
    input_image = add_transparent_padding(input_image, padding)

    width, height = input_image.size
    output_image = Image.new("RGBA", (width, height))

    for x in range(width):
        for y in range(height):
            dx = x - width / 2
            dy = y - height / 2
            distance = math.sqrt(dx**2 + dy**2)
            r = distance * strength

            source_x = int((x - dx * r) % width)
            source_y = int((y - dy * r) % height)

            output_image.putpixel((x, y), input_image.getpixel((source_x, source_y)))

    return output_image

def barrel_distortion(overlay, distortion_amount = 0.1):
    # Define the barrel distortion parameters

    # Apply barrel distortion effect to the overlay image
    width, height = overlay.size
    distorted_overlay = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(distorted_overlay)

    for y in range(height):
        for x in range(width):
            # Calculate polar coordinates relative to the center
            dx = x - width / 2
            dy = y - height / 2
            distance = math.sqrt(dx**2 + dy**2)
            angle = math.atan2(dy, dx)

            # Apply distortion to polar coordinates
            distorted_distance = distance + distortion_amount * distance**2

            # Convert polar coordinates back to Cartesian
            new_x = int(width / 2 + distorted_distance * math.cos(angle))
            new_y = int(height / 2 + distorted_distance * math.sin(angle))

            if 0 <= new_x < width and 0 <= new_y < height:
                draw.point((x, y), overlay.getpixel((new_x, new_y)))
    return distorted_overlay

def elastic_transform(overlay):
    # Elastic Transform
    preprocess = my_transform.RandomElastic(alpha=2, sigma=0.06)
    overlay = preprocess(overlay, mask=None)
    return overlay

def add_gaussian_noise(image, mean=0, std=10):
    """
    Add Gaussian noise to the input PIL image.
    The mean and standard deviation (std) control the distribution of the noise.
    """
    np_image = np.array(image)
    h, w, c = np_image.shape

    # Generate random Gaussian noise with the same shape as the image
    noise = np.random.normal(mean, std, (h, w, c)).astype(np.uint8)

    # Add the noise to the image
    noisy_image = np.clip(np_image + noise, 0, 255).astype(np.uint8)

    # Convert the noisy image back to PIL image
    noisy_pil_image = Image.fromarray(noisy_image)

    return noisy_pil_image

def are_overlapping(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

def generate_non_overlapping_coordinates(existing_coords, width, height, overlay_width, overlay_height):
    max_attempts = 100
    for _ in range(max_attempts):
        x = random.randint(0, width - overlay_width)
        y = random.randint(0, height - overlay_height)
        new_rect = (x, y, overlay_width, overlay_height)
        
        is_overlapping = False
        for existing_rect in existing_coords:
            if are_overlapping(existing_rect, new_rect):
                is_overlapping = True
                break
        
        if not is_overlapping:
            return new_rect
    
    return None