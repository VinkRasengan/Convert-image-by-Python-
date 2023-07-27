from PIL import Image, ImageFilter
import numpy as np
import matplotlib.pyplot as plt

def load_image(file_name):
    try:
        image = Image.open(file_name)
        return image
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None
    except Exception as e:
        print(f"Error occurred while loading the image: {e}")
        return None

def save_image(image, output_file):
    try:
        image.save(output_file)
        print(f"Processed image saved as '{output_file}'")
    except Exception as e:
        print(f"Error occurred while saving the image: {e}")

def adjust_brightness(image, brightness_factor):
    arr = np.array(image)
    adjusted_arr = np.clip(arr * brightness_factor, 0, 255).astype(np.uint8)
    return Image.fromarray(adjusted_arr)

def adjust_contrast(image, contrast_factor):
    arr = np.array(image)
    mean_value = int(np.mean(arr))
    adjusted_arr = np.clip((arr - mean_value) * contrast_factor + mean_value, 0, 255).astype(np.uint8)
    return Image.fromarray(adjusted_arr)

def flip_image(image, direction):
    if direction == "horizontal":
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "vertical":
        return image.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        print("Invalid direction. Please choose 'horizontal' or 'vertical'.")
        return None

def convert_to_grayscale(image):
    arr = np.array(image)
    gray_arr = np.dot(arr[..., :3], [0.2989, 0.5870, 0.1140])
    gray_image = Image.fromarray(gray_arr.astype(np.uint8), 'L')
    return gray_image

def convert_to_sepia(image):
    arr = np.array(image)
    sepia_arr = np.clip(arr.dot([0.393, 0.769, 0.189]) + [40, 20, -20], 0, 255)
    sepia_image = Image.fromarray(sepia_arr.astype(np.uint8))
    return sepia_image

def apply_blur(image):
    return image.filter(ImageFilter.BLUR)

def apply_sharpness(image):
    return image.filter(ImageFilter.SHARPEN)

def crop_center(image, width, height):
    left = (image.width - width) // 2
    top = (image.height - height) // 2
    right = left + width
    bottom = top + height
    return image.crop((left, top, right, bottom))

def crop_circle(image):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, image.width, image.height), fill=255)
    result = Image.new('RGBA', image.size)
    result.paste(image, mask=mask)
    return result

def main():
    file_name = input("Enter the image file name: ")
    image = load_image(file_name)

    if image is None:
        return

    print("Select the image processing function:")
    print("1. Adjust Brightness")
    print("2. Adjust Contrast")
    print("3. Flip Image")
    print("4. Convert to Grayscale/Sepia")
    print("5. Apply Blur/Sharpness")
    print("6. Crop Center")
    print("7. Crop Circle")
    print("0. All functions")

    choice = int(input("Enter your choice: "))

    if choice == 0:
        # Apply all functions
        processed_image = image.copy()

        processed_image = adjust_brightness(processed_image, 1.5)
        save_image(processed_image, f"{file_name.split('.')[0]}_brightness.png")

        processed_image = adjust_contrast(processed_image, 1.5)
        save_image(processed_image, f"{file_name.split('.')[0]}_contrast.png")

        horizontal_flipped_image = flip_image(image, "horizontal")
        save_image(horizontal_flipped_image, f"{file_name.split('.')[0]}_flip_horizontal.png")

        vertical_flipped_image = flip_image(image, "vertical")
        save_image(vertical_flipped_image, f"{file_name.split('.')[0]}_flip_vertical.png")

        gray_image = convert_to_grayscale(image)
        save_image(gray_image, f"{file_name.split('.')[0]}_grayscale.png")

        sepia_image = convert_to_sepia(image)
        save_image(sepia_image, f"{file_name.split('.')[0]}_sepia.png")

        blurred_image = apply_blur(image)
        save_image(blurred_image, f"{file_name.split('.')[0]}_blur.png")

        sharp_image = apply_sharpness(image)
        save_image(sharp_image, f"{file_name.split('.')[0]}_sharp.png")

        cropped_image = crop_center(image, 200, 200)  # Change the crop size as desired.
        save_image(cropped_image, f"{file_name.split('.')[0]}_cropped.png")

        circle_cropped_image = crop_circle(image)
        save_image(circle_cropped_image, f"{file_name.split('.')[0]}_circle_cropped.png")

    elif choice == 1:
        brightness_factor = float(input("Enter the brightness factor: "))
        processed_image = adjust_brightness(image, brightness_factor)
        save_image(processed_image, f"{file_name.split('.')[0]}_brightness.png")

    elif choice == 2:
        contrast_factor = float(input("Enter the contrast factor: "))
        processed_image = adjust_contrast(image, contrast_factor)
        save_image(processed_image, f"{file_name.split('.')[0]}_contrast.png")

    elif choice == 3:
        direction = input("Enter the flip direction ('horizontal' or 'vertical'): ")
        processed_image = flip_image(image, direction)
        if processed_image is not None:
            save_image(processed_image, f"{file_name.split('.')[0]}_flip_{direction.lower()}.png")

    elif choice == 4:
        print("1. Convert to Grayscale")
        print("2. Convert to Sepia")
        conversion_choice = int(input("Enter your choice: "))
        if conversion_choice == 1:
            processed_image = convert_to_grayscale(image)
            save_image(processed_image, f"{file_name.split('.')[0]}_grayscale.png")
        elif conversion_choice == 2:
            processed_image = convert_to_sepia(image)
            save_image(processed_image, f"{file_name.split('.')[0]}_sepia.png")
        else:
            print("Invalid choice. Please choose 1 or 2.")

    elif choice == 5:
        print("1. Apply Blur")
        print("2. Apply Sharpness")
        filter_choice = int(input("Enter your choice: "))
        if filter_choice == 1:
            processed_image = apply_blur(image)
            save_image(processed_image, f"{file_name.split('.')[0]}_blur.png")
        elif filter_choice == 2:
            processed_image = apply_sharpness(image)
            save_image(processed_image, f"{file_name.split('.')[0]}_sharp.png")
        else:
            print("Invalid choice. Please choose 1 or 2.")

    elif choice == 6:
        width = int(input("Enter the width for cropping: "))
        height = int(input("Enter the height for cropping: "))
        processed_image = crop_center(image, width, height)
        save_image(processed_image, f"{file_name.split('.')[0]}_cropped.png")

    elif choice == 7:
        processed_image = crop_circle(image)
        save_image(processed_image, f"{file_name.split('.')[0]}_circle_cropped.png")

    else:
        print("Invalid choice. Please choose a valid option.")

    # Display the processed image
    plt.imshow(processed_image)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()