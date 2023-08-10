import cv2
import numpy as np

def add_fog(image, radius=1000):
    # Generate random fog color
    # fog_color = np.random.randint(0, 256, size=3, dtype=np.uint8)
    fog_color = ((190, 187, 186))
    # Generate random fog density between 0.5 and 0.9
    density = np.random.uniform(0.3, 0.7)
    
    # Create fog overlay
    # image = image[:, :, :3]

    fog_overlay = np.full_like(image, fog_color)
    
    # Create mask for fog effect
    mask = np.zeros_like(image, dtype=np.uint8)
    cv2.circle(mask, (image.shape[1] // 2, image.shape[0] // 2), radius, (255, 255, 255), -1)
    
    # Apply fog effect
    blended_image = cv2.addWeighted(image, 1 - density, fog_overlay, density, 0)
    result = cv2.bitwise_and(blended_image, mask)
    
    return result

