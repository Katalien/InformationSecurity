from collections import Counter

REFERENCE_FREQUENCIES = {
    'а': 0.0801, 'б': 0.0159, 'в': 0.0454, 'г': 0.0165, 'д': 0.0296,
    'е': 0.0845, 'ё': 0.0040, 'ж': 0.0073, 'з': 0.0160, 'и': 0.0734,
    'й': 0.0121, 'к': 0.0349, 'л': 0.0440, 'м': 0.0321, 'н': 0.0670,
    'о': 0.1097, 'п': 0.0281, 'р': 0.0473, 'с': 0.0547, 'т': 0.0626,
    'у': 0.0262, 'ф': 0.0026, 'х': 0.0097, 'ц': 0.0048, 'ч': 0.0144,
    'ш': 0.0073, 'щ': 0.0036, 'ъ': 0.0004, 'ы': 0.0190, 'ь': 0.0174,
    'э': 0.0032, 'ю': 0.0064, 'я': 0.0201
}

ALPHABET = list(REFERENCE_FREQUENCIES.keys())
FREQUENCIES_VALUES = list(REFERENCE_FREQUENCIES.values())

def read_data(filepath):
    with open(filepath, "r",  encoding='utf-8') as file:
        return file.read()


def write_data(filepath, data):
    with open(filepath, "w", encoding='utf-8') as file:
        file.write(data)


def count_matching_index(groupped_text):
    groupped_freqs = Counter(groupped_text)
    total = len(groupped_text)
    if total < 0:
        return 0
    return sum((freq * (freq - 1)) for freq in groupped_freqs.values()) / (total * (total - 1))


def find_key_legth(encrypted_text, max_key_length=30):
    best_ind = 0
    best_length = 1
    for length in range(1, max_key_length + 1):
        groups = []
        for i in range(length):
            group = "".join(encrypted_text[i::length])
            groups.append(group)

        avg_ind = sum(count_matching_index(group) for group in groups) / length
        if avg_ind > best_ind:
            best_ind = avg_ind
            best_length = length
    return best_length


def find_best_letter_shift(group):
    best_shift = 0
    best_score = float('inf')
    for shift in range(len(ALPHABET)):
        shifted_group = ''.join(ALPHABET[(ALPHABET.index(c) - shift) % len(ALPHABET)] for c in group)
        freqs = Counter(shifted_group)
        score = sum( (freq / len(shifted_group) - REFERENCE_FREQUENCIES[char] / 100) ** 2 for char, freq in freqs.items() )
        if score < best_score:
            best_score = score
            best_shift = shift
    return ALPHABET[best_shift]


def decrypt(encrypted_text):
    clean_encrypted_text = ''.join(char.lower() for char in encrypted_text if char.lower() in ALPHABET)

    key_length = find_key_legth(clean_encrypted_text)
    print(f"Длина ключа: {key_length}")

    key = ''
    for i in range(key_length):
        group = ''.join(clean_encrypted_text[j] for j in range(i, len(clean_encrypted_text), key_length))
        key += find_best_letter_shift(group)
    print(f"Найденный ключ: {key}")

    decrypted_text = []
    letter_index = 0

    for char in encrypted_text:
        if char.lower() in ALPHABET:
            shift = ALPHABET.index(key[letter_index % key_length])
            if char.islower():
                decrypted_char = ALPHABET[(ALPHABET.index(char) - shift) % len(ALPHABET)]
            else:
                decrypted_char = ALPHABET[(ALPHABET.index(char.lower()) - shift) % len(ALPHABET)].upper()
            decrypted_text.append(decrypted_char)
            letter_index += 1
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)


def main():
    encrypted_filepath = '../Data/K1_data/K1_encrypted.txt'
    decrypted_filepath = '../Data/K1_data/K1_decrypted.txt'
    encrypted_text = read_data(encrypted_filepath)
    decrypted_text = decrypt(encrypted_text)
    write_data(decrypted_filepath, decrypted_text)
    print(f"Текст записан в директорию {decrypted_filepath}")


if __name__ == "__main__":
    main()