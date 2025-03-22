from utils import *

SIZE_SHIFT = 32


def decode_num_from_bits(bits):
    num = 0
    for i, bit in enumerate(bits):
        num |= (bit << i)
    return num


def bits2bytearray(bits):
    res = bytearray()
    value = 0
    for j, bit in enumerate(bits):
        if j % 8 == 0 and j != 0:
            res.append(value)
            value = 0
        value |= (bit << (j % 8))
    return res


def encode_bits_in_image(image_bytearray, bits):
    res_image = image_bytearray.copy()
    cur_txt_ind = 0
    for i in range(len(res_image)):
        if cur_txt_ind >= len(bits):
            break
        if res_image[i] % 2 != bits[cur_txt_ind]:
            if res_image[i] != 255:
                res_image[i] += 1
            else:
                res_image[i] -= 1
        cur_txt_ind += 1
    return res_image


def encrypt_image(image_bytearray, text_bytearray):
    txt_size = len(text_bytearray)
    res_bits = [(txt_size >> i) & 1 for i in range(SIZE_SHIFT)]
    for c in text_bytearray:
        res_bits += [(c >> i) & 1 for i in range(8)]

    return encode_bits_in_image(image_bytearray, res_bits)


def decrypt_image(image_bytearray):
    txt_size_bits = [image_bytearray[i] % 2 for i in range(SIZE_SHIFT)]
    txt_size = decode_num_from_bits(txt_size_bits)

    txt_bits = []
    for i in range(SIZE_SHIFT, SIZE_SHIFT + (txt_size + 1) * 8):
        txt_bits.append(image_bytearray[i] % 2)

    return bits2bytearray(txt_bits)



def main():
    original_image_path = "../Data/K6_data/original_image.png"
    original_text_path = "../Data/K6_data/original_text.txt"
    output_image_path = "../Data/K6_data/encrypted_image.png"
    output_text_path = "../Data/K6_data/decrypted_text.txt"

    img_bytearray, img_shape = read_image_data(original_image_path)
    text_bytearray = read_text_data(original_text_path, as_bytearray=True)

    encrypted_image = encrypt_image(img_bytearray, text_bytearray)
    write_image_file(output_image_path, encrypted_image, img_shape)
    print(f"Зашифрованное изображение было записано в директории {output_image_path}")

    decrypted_text = decrypt_image(encrypted_image)
    write_text(output_text_path, decrypted_text)
    print(f"Дешифрованный текст был записан в диреторию {output_text_path}")

    print(f"Тексты из файлов совпадают: {test_result(original_text_path, output_text_path)}")


if __name__ == "__main__":
    main()