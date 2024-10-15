# BaseDiscord

A Python implementation of an encoding and decoding algorithm using a custom character set. This library is optimized for safe transmission over Discord, ensuring that encoded messages fit within Discord's character limits and avoid conflicts with markdown and emoji syntax.

## Features

- Custom character set supporting 1,678 Unicode characters.
- Efficient encoding and decoding of binary data.
- Handles zero bytes and large data sequences.
- Ensures encoded messages are compatible with Discord's character limits.
- Average compression ratio of approximately 75%, this is data dependent, and can be further compressed with other compression algorithms.
- Optimized for discord messages, to allow efficient encoding of data through a discord message.
- Checksum Verification: Uses SHA-256 to ensure data integrity during encoding and decoding.
- Maximum Length Flag: Optionally specify a maximum length for encoded messages to prevent exceeding character limits.

## Installation

Clone the repository to your local machine:

```
git clone https://github.com/Silenttttttt/BaseDiscord.git
```

Navigate to the project directory:

```
cd BaseDiscord
```

## Usage

### Encoding Data

To encode binary data, use the `encode_custom` function:

```python
from base_discord import encode_custom

data = b'\x00\x01\x02'  # Example binary data
encoded_message = encode_custom(data)
print(f"Encoded message: {encoded_message}")
```

### Decoding Data

To decode an encoded message back into binary data, use the `decode_custom` function:

```python
from base_discord import decode_custom

encoded_message = "B|A"  # Example encoded message
decoded_data = decode_custom(encoded_message)
print(f"Decoded data: {decoded_data}")
```

## Testing

The library includes tests to verify the encoding and decoding of all possible byte values and each character in the custom character set. To run the tests, execute the script:

```
python base_discord.py
```

### Testing in Main

The `main` function in `base_discord.py` includes comprehensive tests:

1. **Full Byte Range Test**: Encodes and decodes every possible byte value (0-255) to ensure correctness.
2. **CHARSET Verification**: Divides the `CHARSET` into three parts, encodes each part, and verifies the encoding and decoding process through Discord.

To perform the CHARSET verification:
- Run the script and follow the prompts to copy the encoded message.
- Paste the message into Discord and copy it back.
- Paste the copied message into the terminal to verify the encoding and decoding through discord.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss improvements or report bugs. Or directly contact me.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
