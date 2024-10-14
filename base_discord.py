import math

# Define the verified character set, excluding unsupported characters
CHARSET = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    "!@#$%^&()_-+={}[];'\"<>,.?/|~ "
    + ''.join(chr(i) for i in range(0x00A1, 0x02FF))  # Latin Extended and more
    + ''.join(chr(i) for i in range(0x0370, 0x03FF))  # Greek and Coptic
    + ''.join(chr(i) for i in range(0x0400, 0x0485))  # Cyrillic, excluding U+0486 and U+0487
    + ''.join(chr(i) for i in range(0x0488, 0x04FF))  # Continue Cyrillic after U+0487
    + ''.join(chr(i) for i in range(0x0500, 0x052F))  # Cyrillic Supplement
    + ''.join(chr(i) for i in range(0x0530, 0x058F))  # Armenian
    + ''.join(chr(i) for i in range(0x1E00, 0x1EFF))  # Latin Extended Additional
    + ''.join(chr(i) for i in range(0x2100, 0x214F))  # Letterlike Symbols
    + ''.join(chr(i) for i in range(0x2190, 0x21FF))  # Arrows
)
BASE = len(CHARSET)
print(BASE)

def encode_custom(data: bytes) -> str:
    """
    Encodes binary data into a string using a custom base encoding scheme.

    Args:
        data (bytes): The binary data to encode.

    Returns:
        str: The encoded string using the custom character set.
    """
    # Convert the binary data to an integer
    num = int.from_bytes(data, byteorder='big')
    
    # Encode the length of the data
    length_encoded = []
    length = len(data)
    while length > 0:
        length, rem = divmod(length, BASE)
        length_encoded.append(CHARSET[rem])
    
    # Convert the integer to a base-N string, where N is the size of the CHARSET
    encoded = []
    if num == 0:
        encoded.append(CHARSET[0])  # Use the first character to represent zero
    else:
        while num > 0:
            num, rem = divmod(num, BASE)
            encoded.append(CHARSET[rem])
    
    # Reverse the encoded lists and join to form the final string
    return ''.join(reversed(length_encoded)) + '|' + ''.join(reversed(encoded))

def decode_custom(encoded: str) -> bytes:
    """
    Decodes a string encoded with the custom base encoding scheme back into binary data.

    Args:
        encoded (str): The encoded string to decode.

    Returns:
        bytes: The original binary data.
    """
    # Split the encoded string into length and data parts
    length_part, data_part = encoded.split('|', 1)
    
    # Decode the length
    length = 0
    for char in length_part:
        length = length * BASE + CHARSET.index(char)
    
    # Convert the base-N string back to an integer
    num = 0
    if data_part == CHARSET[0]:
        num = 0  # Handle the zero case
    else:
        for char in data_part:
            num = num * BASE + CHARSET.index(char)
    
    # Convert the integer back to bytes
    data = num.to_bytes(length, byteorder='big')
    
    return data

if __name__ == "__main__":
    # Example usage with data that uses every possible byte value
    original_data = bytes(range(256))  # Data containing every possible byte value (0-255)
    encoded_message = encode_custom(original_data)
    print(f"Encoded message: {encoded_message}")

    # Calculate the expansion ratio
    expansion_ratio = len(encoded_message) / len(original_data)
    print(f"Expansion ratio: {expansion_ratio:.2%}")

    # Ensure the encoded message fits within Discord's character limit
    if len(encoded_message) <= 2000:
        print("The message fits within Discord's character limit.")

    # Test encoding and decoding of individual bytes
    for byte in original_data:
        encoded_byte = encode_custom(bytes([byte]))
        decoded_byte = decode_custom(encoded_byte)
        
        # Print results for each byte
        if decoded_byte != bytes([byte]):
            print(f"Mismatch: Original byte: {byte}, Decoded byte: {decoded_byte}")

    print("Encoded message: ", encoded_message)
    user_input = input("Enter the encoded message: ")

    # Decode the full message to verify
    decoded_data = decode_custom(user_input)
    print(f"Decoded data: {decoded_data}")
    assert decoded_data == original_data, "Mismatch: Original data does not match decoded data"

    print("Encoded message length: ", len(user_input))
    print("Original data length: ", len(original_data))

       # Encode and verify each third of the CHARSET
    print("\nEncoding and verifying each third of the CHARSET:")
    third_length = len(CHARSET) // 3

    for part in range(3):
        start_index = part * third_length
        end_index = (part + 1) * third_length if part < 2 else len(CHARSET)
        
        # Create a byte array for the current third
        index_bytes = bytearray()
        for index in range(start_index, end_index):
            # Append the index as a multi-byte sequence
            byte_length = (index.bit_length() + 7) // 8  # Calculate the number of bytes needed
            index_bytes.extend(index.to_bytes(byte_length, byteorder='big'))
        
        # Encode the byte array
        encoded_message = encode_custom(bytes(index_bytes))
        print(f"Encoded CHARSET part {part + 1}: {encoded_message}")

        # Wait for user input to verify the encoding and decoding after Discord
        user_input = input(f"Paste the encoded message for part {part + 1} from Discord: ")
        decoded_data = decode_custom(user_input)
        print(f"Decoded data for part {part + 1}: {decoded_data}")

        # Verify that the decoded data matches the original indices
        current_pos = 0
        for index in range(start_index, end_index):
            byte_length = (index.bit_length() + 7) // 8
            expected_bytes = index.to_bytes(byte_length, byteorder='big')
            actual_bytes = decoded_data[current_pos:current_pos + byte_length]
            assert actual_bytes == expected_bytes, f"Mismatch: Original index: {index}, Decoded byte: {actual_bytes}"
            current_pos += byte_length

    print("All tests successful!")