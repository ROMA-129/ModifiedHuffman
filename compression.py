# ==================================================
# File: compression.py
# Purpose:
# - Compress the input text using the generated Huffman codes.
# - Encode the text into a sequence of bits.
# - Store the compressed data in a binary file.
# - Preserve any metadata required for decompression.
# ==================================================


import huffman

# 1. حساب التكرارات والاحتمالات
frequencies = huffman.calculate_frequencies(data)
probabilities = huffman.calculate_probabilities(frequencies, len(data))

# 2. تطبيق الحد وتجميع Others
filtered, others = huffman.apply_probability_limit(probabilities, min_limit)

# 3. بناء الشجرة والأكواد
tree = huffman.build_huffman_tree(filtered)
main_codes = huffman.generate_huffman_codes(tree)
original_codes, fixed_length = huffman.generate_original_codes(frequencies.keys())