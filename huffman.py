from collections import Counter
import heapq
from itertools import count


# --------------------------------------------------
# 1. Calculate Frequencies
# --------------------------------------------------

def calculate_frequencies(text):
    return dict(Counter(text))


# --------------------------------------------------
# 2. Calculate Probabilities
# --------------------------------------------------

def calculate_probabilities(frequencies):
    total = sum(frequencies.values())

    if total == 0:
        return {}

    return {
        char: freq / total
        for char, freq in frequencies.items()
    }


# --------------------------------------------------
# 3. Apply Minimum Probability Limit
# --------------------------------------------------

def apply_probability_limit(probabilities, min_limit):
    filtered = {}
    others = {}

    for char, prob in probabilities.items():

        if prob <= min_limit:
            others[char] = prob

        else:
            filtered[char] = prob

    if others:
        filtered["Others"] = sum(others.values())

    return filtered, others


# --------------------------------------------------
# 4. Build Huffman Tree
# --------------------------------------------------

def build_huffman_tree(probabilities):

    if not probabilities:
        return None

    heap = []
    order = count()

    for char, prob in probabilities.items():
        heapq.heappush(
            heap,
            (prob, next(order), char)
        )

    while len(heap) > 1:

        prob1, _, left = heapq.heappop(heap)
        prob2, _, right = heapq.heappop(heap)

        new_node = (left, right)

        heapq.heappush(
            heap,
            (
                prob1 + prob2,
                next(order),
                new_node
            )
        )

    return heap[0][2]


# --------------------------------------------------
# 5. Generate Huffman Codes
# --------------------------------------------------

def generate_huffman_codes(tree):

    codes = {}

    def traverse(node, code):

        if isinstance(node, str):
            codes[node] = code or "0"
            return

        left, right = node

        traverse(left, code + "0")
        traverse(right, code + "1")

    if tree is not None:
        traverse(tree, "")

    return codes


# --------------------------------------------------
# 6. Generate Codes for Others Symbols
# --------------------------------------------------

def generate_others_codes(others):

    if not others:
        return {}

    total = sum(others.values())

    normalized_probabilities = {
        char: prob / total
        for char, prob in others.items()
    }

    others_tree = build_huffman_tree(
        normalized_probabilities
    )

    return generate_huffman_codes(others_tree)


# --------------------------------------------------
# 7. Complete Huffman Processing
# --------------------------------------------------

def process_huffman(text, min_limit):

    frequencies = calculate_frequencies(text)

    probabilities = calculate_probabilities(
        frequencies
    )

    filtered, others = apply_probability_limit(
        probabilities,
        min_limit
    )

    tree = build_huffman_tree(filtered)

    codes = generate_huffman_codes(tree)

    others_codes = generate_others_codes(others)

    return {
        "frequencies": frequencies,
        "probabilities": probabilities,
        "filtered": filtered,
        "others": others,
        "tree": tree,
        "codes": codes,
        "others_codes": others_codes
    }


