import heapq


# 1. Calculate frequencies
def calculate_frequencies(data):
    frequencies = {}

    for symbol in data:
        if symbol in frequencies:
            frequencies[symbol] += 1
        else:
            frequencies[symbol] = 1

    return frequencies


# 2. Calculate probabilities
def calculate_probabilities(frequencies, total):
    probabilities = {}

    if total == 0:
        return probabilities

    for symbol in frequencies:
        probabilities[symbol] = frequencies[symbol] / total

    return probabilities


# 3. Apply Minimum Probability Limit
def apply_probability_limit(probabilities, min_limit):
    filtered = {}
    others = {}

    for symbol in probabilities:
        if probabilities[symbol] <= min_limit:
            others[symbol] = probabilities[symbol]
        else:
            filtered[symbol] = probabilities[symbol]

    if others:
        filtered["Others"] = sum(others.values())

    return filtered, others


# 4. Build Huffman Tree
def build_huffman_tree(probabilities):
    if not probabilities:
        return None

    heap = []
    order = 0

    for symbol in probabilities:
        heapq.heappush(
            heap,
            (probabilities[symbol], order, symbol)
        )
        order += 1

    while len(heap) > 1:
        p1, _, left = heapq.heappop(heap)
        p2, _, right = heapq.heappop(heap)

        parent = (left, right)

        heapq.heappush(
            heap,
            (p1 + p2, order, parent)
        )
        order += 1

    return heap[0][2]


# 5. Generate Huffman Codes
def generate_huffman_codes(tree):
    codes = {}

    def traverse(node, code):
        if not isinstance(node, tuple):
            codes[node] = code if code else "0"
            return

        traverse(node[0], code + "0")
        traverse(node[1], code + "1")

    if tree is not None:
        traverse(tree, "")

    return codes


# 6. Generate Original Fixed-Length Codes
def generate_original_codes(symbols):
    symbols = sorted(symbols)

    # At least one bit is used, including the one-symbol case.
    length = max(1, (len(symbols) - 1).bit_length())

    codes = {}

    for index, symbol in enumerate(symbols):
        codes[symbol] = format(index, "0{}b".format(length))

    return codes, length