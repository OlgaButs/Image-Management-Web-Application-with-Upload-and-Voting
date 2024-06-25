import math
from PIL import Image, ImageFilter, ImageEnhance


def image_processing(input_path, output_path, select):
    """
    Perform image processing based on the selected option.
    """
    try:
        image = Image.open(input_path)
    except FileNotFoundError:
        print("Input file not found.")
    try:
        if select != '0':
            new_image = choice(int(select), image)
            new_image.save(output_path)
    except Exception as e:
        print("Image processing error: " + str(e))


def choice(sel, image):
    """
    Apply the chosen image processing operation on the input image.
    """
    if sel == 1:
        return apply_vignette(image, image.width // 2, image.height // 2)
    
    elif sel == 2:
        # Convert image to grayscale
        image = image.convert("L")
        # Apply edge detection using a Laplacian kernel
        return image.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0))
    
    elif sel == 3:
        return apply_sepia(image)
    
    elif sel == 4:
        # Decrease color intensity
        converter = ImageEnhance.Color(image)
        return converter.enhance(0.5)
    
    elif sel == 5:
        # Increase color intensity
        converter = ImageEnhance.Color(image)
        return converter.enhance(2)
    
    elif sel == 6:
        # Multiply image intensity by a factor of 2
        return multiply_intensity(image, 2)
    
    elif sel == 7:
        # Multiply image intensity by a factor of 0.5
        return multiply_intensity(image, 0.5)
    
    elif sel == 8:
        # Convert image to grayscale using an alternative method
        return effect_gray(image)
    
    elif sel == 9:
        # Create a negative image
        return create_negative_image(image)
    
    elif sel == 10:
        # Swap color channels (Red and Green)
        return swap_color_channels(image)
    
    elif sel == 11:
        # Apply edge enhancement filter
        return image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
    elif sel == 12:
        # Apply a combination of grayscale, smoothing, and embossing
        img_gray = image.convert("L")
        img_gray_smooth = img_gray.filter(ImageFilter.SMOOTH)
        return img_gray_smooth.filter(ImageFilter.EMBOSS)
    
    else:
        return "Something's wrong"


def apply_vignette(image, xref, yref):
    """
    Apply a vignette effect to the image.
    """
    width, height = image.size
    new_image = Image.new(image.mode, image.size)
    
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            
            factor = get_factor(x, y, xref, yref)
            pixel = tuple(int(channel * factor) for channel in pixel)
            
            new_image.putpixel((x, y), pixel)
    return new_image


def get_factor(x, y, xref, yref):
    """
    Calculate the vignette factor based on the distance from the reference point.
    """
    distance = math.sqrt((x - xref)**2 + (y - yref)**2)
    distance_to_edge = math.sqrt(xref**2 + yref**2)
    return 1 - (distance / distance_to_edge)


def apply_sepia(image):
    """
    Apply sepia tone effect to the image.
    """
    width, height = image.size
    new_image = Image.new(image.mode, image.size)
    
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            r = int(0.189 * pixel[0] + 0.769 * pixel[1] + 0.393 * pixel[2])
            g = int(0.168 * pixel[0] + 0.686 * pixel[1] + 0.349 * pixel[2])
            b = int(0.131 * pixel[0] + 0.534 * pixel[1] + 0.272 * pixel[2])
            new_image.putpixel((x, y), (r, g, b))
    
    return new_image


def multiply_intensity(im, factor):
    """
    Multiply the intensity of the Y channel of the image by a given factor.
    """
    new_im = im.convert("YCbCr")
    width, height = im.size

    for x in range(width):
        for y in range(height):
            pixel = new_im.getpixel((x, y))
            py = min(255, int(pixel[0] * factor))  # Multiply the Y channel by the factor
            new_im.putpixel((x, y), (py, pixel[1], pixel[2]))
    
    result = new_im.convert("RGB")
    return result


def effect_gray(image):
    """
    Convert the image to grayscale by taking the average of the color channels.
    """
    width, height = image.size
    new_im = Image.new("L", image.size)
    
    for x in range(width):
        for y in range(height):
            p = image.getpixel((x, y))
            # Combine colors (e.g., average of R, G, and B components)
            l = int((p[0] + p[1] + p[2]) // 3)
            
            new_im.putpixel((x, y), (l,))
    
    return new_im


def create_negative_image(image):
    """
    Create a negative image by subtracting each color channel from 255.
    """
    width, height = image.size
    new_image = Image.new(image.mode, image.size)
    
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            red = 255 - pixel[0]
            green = 255 - pixel[1]
            blue = 255 - pixel[2]
            new_image.putpixel((x, y), (red, green, blue))
    
    return new_image


def swap_color_channels(image):
    width, height = image.size
    new_image = Image.new(image.mode, image.size)
    
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            red = pixel[1]
            green = pixel[0]
            blue = pixel[2]
            new_image.putpixel((x, y), (red, green, blue))

    image = image.convert('RGB')

    pixels = image.load()
    width, height = image.size
    
    return new_image
