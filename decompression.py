import json

def read_compressed_file(filename):
    with open(filename, "rb") as file:
        header_length = int.from_bytes(file.read(4), "big")

        overhead = json.loads(
            file.read(header_length).decode("utf-8")
        )

        data = file.read()

    return overhead, data


def bytes_to_bits(data, padding):

    bits = ""
    for byte in data:
        bits = bits + format(byte, "08b")

    if padding > 0:
        bits = bits[:-padding]

    return bits


def swap_table(table):
    
    swapped = {}

    for symbol in table:
        swapped[table[symbol]] = symbol

    return swapped


def decode_bits(bits, codes, original_codes, original_length):

    code_to_symbol = swap_table(codes)
    original_to_symbol = swap_table(original_codes)

    result = []
    current = ""        
    position = 0        

    while position < len(bits):
    
        current = current + bits[position]
        position = position + 1

        
        if current in code_to_symbol:
            symbol = code_to_symbol[current]
            current = ""

            
            if symbol == "Others":
                fixed_code = bits[position:position + original_length]
                position = position + original_length

                if fixed_code not in original_to_symbol:
                    print("Error: unknown fixed-length code", fixed_code)
                    return "".join(result)

                symbol = original_to_symbol[fixed_code]

            result.append(symbol)

    if current != "":
        print("Warning: the last bits did not match any code")

    return "".join(result)


def decompress_to_text(input_filename):

    overhead, data = read_compressed_file(input_filename)
    bits = bytes_to_bits(data, overhead["padding"])

    return decode_bits(
        bits,
        overhead["main_codes"],
        overhead["others_codes"],
        overhead["fixed_length"]
    )


def decompress_file(input_filename, output_filename):

    text = decompress_to_text(input_filename)

    # newline="" keeps \r\n exactly as it was, utf-8 keeps Arabic safe
    with open(output_filename, "w", encoding="utf-8", newline="") as file:
        file.write(text)

    print("Decompressed '" + input_filename + "' into '" + output_filename + "' successfully.")
