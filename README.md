# COCO-traffic-sign-dataset-generator
This Python script generates a synthetic dataset of traffic sign images in COCO format, intended for training and testing object detection models. The dataset includes various traffic sign overlays placed on diverse background images, offering a wide range of scenarios to enhance model robustness.

## Features

- Generates synthetic traffic sign images by overlaying them on different backgrounds.
- Applies augmentation techniques to both the traffic sign overlays and the background images.
- Supports resizing of images to specified dimensions.
- Provides customizable options for generating the dataset.
- Generates COCO-style JSON annotations for each image.

## Requirements

- Python 3.x
- Required Python libraries: `PIL`, `numpy`

## Usage

1. Clone this repository to your local machine.
2. Prepare your overlay images (traffic signs) and background images. Place them in the signs and backgrounds folders respectively.
3. Run the script with the desired command-line arguments. For example:

``` bash
python main.py --number_of_images 100 --width 240 --height 180 --resize
```
This command generates 100 synthetic images with a width of 240 pixels and height of 180 pixels.

4. The generated images will be saved in the output/images folder, and the COCO-style annotations will be saved in the output/annotations folder.

## Customization
You can customize the script's behavior using the following command-line arguments:

- `--number_of_images`: Number of synthetic images to generate.
- `--width and --height`: Dimensions to which images will be resized.
- `--resize`: Whether to resize the images.
- `--overlays_path`: Path to traffic sign overlay images.
- `--backgrounds_path`: Path to background images.
- `--images_save_path`: Path to save generated images.
- `--annotation_save_path`: Path to save annotation JSON files.
- `--annotation_filename`: Name of the annotation JSON file.

## Dataset Structure
The generated dataset follows the COCO (Common Objects in Context) dataset structure. The dataset information is stored in a JSON file, including images, categories, and annotations.

## Contributing
Contributions to improve and extend this dataset generator are welcome! If you find any issues or have suggestions for enhancements, please feel free to submit a pull request or open an issue.

