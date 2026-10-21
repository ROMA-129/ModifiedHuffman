# ==================================================
# File: compression.py
# Purpose:
# - Compress the input text using the generated Huffman codes.
# - Encode the text into a sequence of bits.
# - Store the compressed data in a binary file.
# - Preserve any metadata required for decompression.
# ==================================================

import json
import huffman


# Read input file
def read_input_file(input_path):
    with open(input_path, "r", encoding="utf-8", newline="") as file:
        return file.read()


# Encode text into a string of bits
def encode_data(data, main_codes, original_codes, others):
    bits = ""

    for symbol in data:
        if symbol in others:
            # rare symbol: "Others" code + its fixed-length code
            bits += main_codes["Others"] + original_codes[symbol]
        else:
            bits += main_codes[symbol]

    return bits


# Convert bits into bytes
def convert_bits_to_bytes(bits):
    # fill the last byte with zeros
    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding

    packed = bytearray()

    for i in range(0, len(bits), 8):
        packed.append(int(bits[i:i + 8], 2))

    return bytes(packed), padding


# Create header (data needed for decompression)
def create_header(total, padding, main_codes, original_codes, fixed_length, others):
    others_codes = {}

    for symbol in others:
        others_codes[symbol] = original_codes[symbol]

    header = {
        "total": total,
        "padding": padding,
        "fixed_length": fixed_length,
        "main_codes": main_codes,
        "others_codes": others_codes
    }

    return json.dumps(header).encode("utf-8")


# Write compressed binary file
def write_compressed_file(output_path, header, packed):
    with open(output_path, "wb") as file:
        file.write(len(header).to_bytes(4, "big"))
        file.write(header)
        file.write(packed)


# Compress
def compress(input_path, output_path, min_limit):
    data = read_input_file(input_path)

    frequencies = huffman.calculate_frequencies(data)
    probabilities = huffman.calculate_probabilities(frequencies, len(data))

    filtered, others = huffman.apply_probability_limit(probabilities, min_limit)

    tree = huffman.build_huffman_tree(filtered)
    main_codes = huffman.generate_huffman_codes(tree)
    original_codes, fixed_length = huffman.generate_original_codes(frequencies.keys())

    bits = encode_data(data, main_codes, original_codes, others)
    packed, padding = convert_bits_to_bytes(bits)
    header = create_header(len(data), padding, main_codes,
                           original_codes, fixed_length, others)

    write_compressed_file(output_path, header, packed)
