import numpy as np
import cv2


def read_image_data(filepath):
    image = cv2.imread(filepath)
    return bytearray(image.tobytes()), image.shape


def read_text_data(filepath, as_bytearray=False):
    mode = 'rb' if as_bytearray else 'r'
    with open(filepath, mode) as file:
        text = file.read()
        return bytearray(text) if as_bytearray else text


def write_image_file(image_filepath, image_bytearray, image_shape):
    image_data = np.frombuffer(image_bytearray, dtype=np.uint8)
    image = image_data.reshape(image_shape)
    cv2.imwrite(image_filepath, image)


def write_text(text_filepath, text_bytearray):
    text = text_bytearray.decode('utf-8')
    with open(text_filepath, 'w', encoding='utf-8', newline='') as file:
        file.write(text)


def test_result(original_text_path, decrypted_text_path):
    original_text = read_text_data(original_text_path)
    decrypted_text = read_text_data(decrypted_text_path)
    return original_text == decrypted_text
