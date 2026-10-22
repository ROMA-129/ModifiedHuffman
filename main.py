import compression
import decompression

while True:
    print("\n1. Compress")
    print("2. Decompress")
    print("3. Exit")

    choice = input("Enter your choice (1, 2 or 3): ")

    if choice == "1":
        input_file = input("Enter input file: ")
        output_file = input("Enter compressed file name: ")
        limit = float(input("Enter minimum probability limit (0 to 1): "))

        if 0 <= limit <= 1:
            compression.compress(input_file, output_file, limit)
            print("Compression completed successfully!")
        else:
            print("Invalid probability limit!")

    elif choice == "2":
        input_file = input("Enter compressed file name: ")
        output_file = input("Enter output file name: ")

        decompression.decompress_file(input_file, output_file)

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice! Try again.")