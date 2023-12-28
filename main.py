import cv2
import numpy as np

def uerd_encode(cover_image, secret_data):
    """Encodes secret data into a cover image using the UERD steganography algorithm."""
    secret_data_len = len(secret_data) * 8
    cover_image_width, cover_image_height, _ = cover_image.shape
    stego_image = np.zeros((cover_image_width, cover_image_height, 3), dtype=np.uint8)

    for i in range(secret_data_len):
        pixel_index, bit_position = divmod(i, 3)

        # Convert pixel to float32 before applying DCT
        pixel_float32 = cover_image[pixel_index].astype(np.float32)
        dct_coefficients = cv2.dct(pixel_float32)

        threshold = np.mean(dct_coefficients)
        if secret_data[i // 8] == '1':
            dct_coefficients[0, bit_position] += 1  # Only modify the specified DCT coefficient
        else:
            dct_coefficients[0, bit_position] -= 1  # Only modify the specified DCT coefficient

        # Convert back to float32 after applying IDCT
        stego_image[pixel_index] = cv2.idct(dct_coefficients).astype(np.uint8)

    return stego_image

def uerd_decode(stego_image):
    """Decodes secret data from a stego image using the UERD steganography algorithm."""
    secret_data = ""
    secret_data_len = len(stego_image) * 3 * 8
    num_pixels = len(stego_image)

    for i in range(secret_data_len):
        pixel_index, bit_position = divmod(i, 3)

        # Ensure pixel_index is within the valid range
        if pixel_index >= num_pixels:
            break
        # Convert pixel to float32 before applying DCT
        pixel_float32 = stego_image[pixel_index].astype(np.float32)
        dct_coefficients = cv2.dct(pixel_float32)

        threshold = np.mean(dct_coefficients)
        secret_data += str(int(dct_coefficients[0, bit_position] > threshold))

    return secret_data

def representation_data(data):
    # Check for non-printable characters and their positions
    non_printable_positions = [(i, ord(char)) for i, char in enumerate(data) if not char.isprintable()]

    if non_printable_positions:
        print("Non-printable characters found at positions:")
        for position, char_code in non_printable_positions:
            print(f"Position: {position}, Character Code: {char_code}")

    # Check the length of the data
    print(f"Data Length: {len(data)}")

    # Print the data as both ASCII and binary
    print("ASCII Representation:")
    for char in data:
        print(f"{char} ({ord(char)})")

    print("Binary Representation:")
    binary_data = ' '.join(format(ord(char), '08b') for char in data)
    print(binary_data)

# Example data (replace this with your actual data)
data = "LOGANATHAVISHNUBALAJI"

# Encode the data
cover_image = cv2.imread("/content/Picture1.png")  # Replace with the path to your cover image
stego_image = uerd_encode(cover_image, data)

# Save the stego image
cv2.imwrite("stego_image.png", stego_image)

# Decode the data from the stego image
decoded_data = uerd_decode(stego_image)

# Debug the decoded data
representation_data(data)
