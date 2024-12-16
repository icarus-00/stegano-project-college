import argparse

# Convert text message to binary, keeping all whitespace characters (spaces, tabs, newlines)
def text_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

# Convert binary data back to text, restoring all whitespace characters
def binary_to_text(binary_data):
    message = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
    return message

# Hide the message (binary encoded) in the text file, including whitespaces
def hide_message_using_binary(text_file, secret_message):
    binary_message = text_to_binary(secret_message)
    
    with open(text_file, 'r') as file:
        content = file.read()
    
    # Embed binary message at the end of the content (for simplicity)
    content += '\n' + binary_message

    with open(text_file, 'w') as file:
        file.write(content)
    
    print("Message hidden using binary encoding!")

# Extract the hidden binary message from the text file and decode it back to text
def extract_hidden_message_from_binary(text_file):
    with open(text_file, 'r') as file:
        content = file.readlines()
    
    # Assuming the binary message is the last line of the file
    binary_message = content[-1].strip()  # Strip any trailing whitespace/newline
    secret_message = binary_to_text(binary_message)
    return secret_message

# Main function to handle the command-line interface
def main():
    parser = argparse.ArgumentParser(description="Advanced Text File Steganography Tool")
    
    # The 'action' argument determines whether to hide or extract the message
    parser.add_argument('action', choices=['hide', 'extract'], help="Action to perform: 'hide' or 'extract'")
    
    # 'text_file' is the file to hide/extract the message in/from
    parser.add_argument('text_file', help="Text file to hide/extract message from")
    
    # 'message' is only required for the 'hide' action
    parser.add_argument('message', nargs='?', help="Message to hide (only for 'hide' action)")

    args = parser.parse_args()

    # If the action is 'hide', make sure a message is provided
    if args.action == 'hide':
        if args.message:
            hide_message_using_binary(args.text_file, args.message)
        else:
            print("Error: Message required for hiding.")
    
    # If the action is 'extract', simply extract the hidden message
    elif args.action == 'extract':
        message = extract_hidden_message_from_binary(args.text_file)
        print(f"Extracted message: {message}")

# Ensure that this script is run directly
if __name__ == "__main__":
    main()
