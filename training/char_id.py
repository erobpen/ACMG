import json

def convert_to_jsonl(input_file, output_file):
    """
    Robustly convert a complex JSON file to JSONL format.
    
    Args:
    input_file (str): Path to the input JSON file
    output_file (str): Path to the output JSONL file
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        # Read the entire file content
        content = f.read()
    
    try:
        # Try to parse the entire content
        data = json.loads(content)
    except json.JSONDecodeError:
        # If that fails, try to parse as a document with source
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(content)
            document = root.find('document')
            if document is not None:
                content = document.find('document_content').text
                data = json.loads(content)
        except Exception as e:
            print(f"Failed to parse file: {e}")
            return
    
    # Ensure we're working with a list of dictionaries
    if not isinstance(data, list):
        data = [data]
    
    with open(output_file, 'w', encoding='utf-8') as out:
        for item in data:
            # Ensure we extract the 'messages' list
            messages = item.get('messages', item)
            
            # Write each message as a separate JSONL line
            json.dump({"messages": messages}, out)
            out.write('\n')
    
    print(f"Converted {input_file} to JSONL format. Output saved to {output_file}")

# Example usage
input_file = 'C:\\Users\\pavle\\OneDrive - fer.hr\\Desktop\\acmg\\training\\nesto3.json'  # Replace with your input file name
output_file = 'output.jsonl'  # Replace with desired output file name

convert_to_jsonl(input_file, output_file)