import os
from PIL import Image

def resize_images(input_dir, output_dir, width, height):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # List all files in the input directory
    files = os.listdir(input_dir)
    
    # Iterate over each file in the input directory
    for file in files:
        try:
            # Open the image file
            image_path = os.path.join(input_dir, file)
            img = Image.open(image_path)
            
            # Resize the image
            img.thumbnail((width, height))
            
            # Save the resized image to the output directory
            output_path = os.path.join(output_dir, file)
            img.save(output_path)
            
            print(f"Resized {file} and saved to {output_path}")
        
        except Exception as e:
            print(f"Error resizing {file}: {e}")

# Example usage:
if __name__ == "__main__":
    # Define input and output directories
    input_directory = "/Users/rohansridhar/Desktop/cv/object_detection/output/train/augmented_data"
    output_directory = "/Users/rohansridhar/Desktop/cv/object_detection/output/resized_train"
    
    # Define the desired width and height
    desired_width = 256
    desired_height = 256
    
    # Resize images
    resize_images(input_directory, output_directory, desired_width, desired_height)
