

def replace_newlines(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        # Read the entire content of the file
        content = infile.read()
    
    # Replace actual newline characters with the string '\n'
    modified_content = content.replace("\n", "\\n")
    
    # Write the modified content to the new file
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(modified_content)

# Replace with your actual file paths
input_filepath = "note.txt"    # Input file path
output_filepath = "output.txt"  # Output file path

replace_newlines(input_filepath, output_filepath)

print(f"File written with \\n replacements to {output_filepath}")
