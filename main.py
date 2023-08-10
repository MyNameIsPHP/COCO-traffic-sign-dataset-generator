import random
import os
import json
import numpy as np
from PIL import Image
from add_rain import *
from add_sun import *
from add_snow import *
from add_fog import *
from basic_augmentation import *
import argparse

# Create COCO dataset structure
coco_dataset = {
    "images": [],
    "categories": [],
    "annotations": []
}

# Define category IDs for traffic sign categories
categories_dict = {
    "stop": 1,
    "left": 2,
    "right": 3,
    "straight": 4,
    "no_left": 5,
    "no_right": 6
}

def add_annotation(image_id, category_id, bbox):
    annotation = {
        "id": len(coco_dataset["annotations"]) + 1,
        "image_id": image_id,
        "bbox": bbox,  # [x, y, width, height]
        "area": bbox[2] * bbox[3],
        "iscrowd": 0,
        "category_id": category_id,
        "segmentation": []
    }
    coco_dataset["annotations"].append(annotation)

def add_image(file_name, height, width):
    image = {
        "file_name": file_name,
        "height": height,
        "width": width,
        "id": len(coco_dataset["images"])
    }
    coco_dataset["images"].append(image)

def main(opt):
   
    # Add category entries to the COCO dataset
    for key in categories_dict:
        category = {
            "supercategory": "trafficsign",
            "id": categories_dict[key],
            "name": key
        }
        coco_dataset['categories'].append(category)

    folder_A = opt.overlays_path
    folder_B = opt.backgrounds_path
    output_folder = opt.images_save_path

    overlay_images_list = [f for f in os.listdir(folder_A) if f.endswith(('.png', '.jpg', '.jpeg'))]
    background_images_list = [f for f in os.listdir(folder_B) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if not overlay_images_list or not background_images_list:
        print("No images found in the specified folders.")
        return

    number_of_outputs = opt.number_of_images

    for idx in range(number_of_outputs):
        selected_background = random.choice(background_images_list)
        number_of_signs = random.randint(1, 3)
        os.makedirs(output_folder, exist_ok=True)
        
        background_path = os.path.join(folder_B, selected_background)
        background = Image.open(background_path)
        
        if opt.resize:
            background = background.resize((opt.width, opt.height))
            
        bg_width, bg_height = background.size

        existing_coords = []

        for i in range(number_of_signs):
            selected_overlay = random.choice(overlay_images_list)
            overlay_path = os.path.join(folder_A, selected_overlay)
            overlay = Image.open(overlay_path).convert("RGBA")
            overlay_width, overlay_height = overlay.size

            # Apply common augmentation techniques
            common_techniques = ['adjust_brightness', 'adjust_contrast', 'random_rotate', 'apply_occlusion', 'apply_shear']
            chosen_common_techniques = random.sample(common_techniques, random.randint(0, 5))

            for technique in chosen_common_techniques:
                try:
                    if technique == 'adjust_brightness':
                        overlay = adjust_brightness(overlay, random.uniform(0.4, 1.6))
                    elif technique == 'adjust_contrast':
                        overlay = adjust_contrast(overlay, random.uniform(0.4, 1.6))
                    elif technique == 'random_rotate':
                        overlay = random_rotate(overlay, -30, 30)
                    elif technique == 'apply_shear':
                        overlay = apply_shear(overlay, padding=overlay_width, shear_factor=random.uniform(-0.5, 0.5))
                    elif technique == 'apply_occlusion':
                        overlay = apply_occlusion(overlay, occlusion_size=(random.randint(int(overlay_width / 8), int(overlay_width / 3)), random.randint(int(overlay_height / 8), int(overlay_height / 3))))
                    overlay = remove_transparent_padding(overlay)
                except Exception as e:
                    print(f"Error in {technique}: {e}")

            # Apply distortion techniques
            distortion_techniques = ['elastic', 'pincushion', 'barrel']
            chosen_distortion_techniques = random.sample(distortion_techniques, random.randint(0, 1))

            for technique in chosen_distortion_techniques:
                try:
                    if technique == 'pincushion':
                        overlay = pincushion_distortion(overlay, padding=overlay_width, strength=random.uniform(0.001, 0.0016))
                    elif technique == 'barrel':
                        overlay = barrel_distortion(overlay, distortion_amount=random.uniform(0.001, 0.3))
                    elif technique == 'elastic':
                        overlay = elastic_transform(overlay)
                    overlay = remove_transparent_padding(overlay)
                except Exception as e:
                    print(f"Error in {technique}: {e}")

            output_size = random.randint(int(bg_width / 12), int(bg_width / 4))
            overlay = overlay.resize((output_size, output_size))
            overlay_width, overlay_height = overlay.size

            # Generate non-overlapping coordinates
            new_coordinates = generate_non_overlapping_coordinates(existing_coords, bg_width, bg_height, overlay_width, overlay_height)

            while new_coordinates is None:
                new_coordinates = generate_non_overlapping_coordinates(existing_coords, bg_width, bg_height, overlay_width, overlay_height)

            existing_coords.append(new_coordinates)

            output_path = os.path.join(output_folder, f"{idx}_{i}.png")
            background.paste(overlay, new_coordinates[:2], overlay)

            image_id = len(coco_dataset["images"])
            temp = overlay_path.split("_")
            if len(temp) == 3:
                category_name = temp[0].split("/")[1] + "_" + temp[1]
            else:
                category_name = temp[0].split("/")[1]
            category_id = categories_dict[category_name]
            bbox = [new_coordinates[0], new_coordinates[1], overlay_width, overlay_height]

            add_annotation(image_id, category_id, bbox)

        # Apply background augmentation techniques
        background_techniques = ['adjust_brightness', 'adjust_contrast', 'add_gaussian_noise', 'add_rain', 'add_sun', 'add_snow', 'add_fog']
        chosen_background_techniques = random.sample(background_techniques, 1)

        for technique in chosen_background_techniques:
            try:
                if technique == 'adjust_brightness':
                    background = adjust_brightness(background, random.uniform(0.4, 1.6))
                elif technique == 'adjust_contrast':
                    background = adjust_contrast(background, random.uniform(0.4, 1.6))
                elif technique == 'add_gaussian_noise':
                    background = add_gaussian_noise(background, mean=random.uniform(0, 1), std=random.uniform(0, 1))
                elif technique == 'add_rain':
                    np_image = np.array(background)
                    np_image_copy = np_image.copy()
                    np_result = add_rain(np_image_copy, drop_length = random.randint(5, int(background.height/14)))
                    background = Image.fromarray(np_result)
                elif technique == 'add_sun':
                    background = apply_sunny_effect(background)
                elif technique == 'add_snow':
                    np_image = np.array(background)
                    np_image_copy = np_image.copy()
                    np_result = add_snow(np_image_copy)
                    background = Image.fromarray(np_result)
                elif technique == 'add_fog':
                    np_image = np.array(background.convert("RGB"))
                    np_image_copy = np_image.copy()
                    np_result = add_fog(np_image_copy)
                    background = Image.fromarray(np_result)
            except Exception as e:
                print(f"Error in {technique}: {e}")

        output_path = os.path.join(output_folder, f"{idx}.png")
        background.save(output_path, "PNG")
        add_image(f"{idx}.png", background.height, background.width)
        print("Saved", output_path)

    # Save COCO JSON file
    if not os.path.exists(opt.annotation_save_path):
        os.makedirs(opt.annotation_save_path)
        print(f"Directory '{opt.annotation_save_path}' created.")
    else:
        print(f"Directory '{opt.annotation_save_path}' already exists.")

    coco_json_path = os.path.join(opt.annotation_save_path, opt.annotation_filename + ".json")
    with open(coco_json_path, "w") as coco_json_file:
        json.dump(coco_dataset, coco_json_file)
    print("Done !!!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Traffic Sign COCO dataset generator")
    parser.add_argument("--resize", action="store_true", help="resize the image or not")
    parser.add_argument("--width", type=int, default=240, help="width that result images will be resized to")
    parser.add_argument("--height", type=int, default=180, help="height that result image will be resized to")
    parser.add_argument("--number_of_images", type=int, default=100, help="number of images the code will generate")
    parser.add_argument("--overlays_path", type=str, default="signs", help="path to traffic signs overlay images that will be added to backgrounds")
    parser.add_argument("--backgrounds_path", type=str, default="backgrounds", help="path to background images")
    parser.add_argument("--images_save_path", type=str, default="output/images", help="path to save images")
    parser.add_argument("--annotation_save_path", type=str, default="output/annotations", help="path to annotation JSON file")
    parser.add_argument("--annotation_filename", type=str, default="annotation", help="path to annotation JSON file")
    
    opt = parser.parse_args()
    if not os.path.exists(opt.images_save_path):
        os.makedirs(opt.annotation_save_path)
        print(f"Directory '{opt.images_save_path}' created.")
    else:
        print(f"Directory '{opt.images_save_path}' already exists.")
    main(opt)
