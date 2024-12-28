

import json

def parse_conversation(input_string):
    """
    Parse a conversation string into a list of dictionaries with role and content.
    
    Args:
        input_string (str): A string containing conversation turns marked with 'Bot:' and 'Me:'
    
    Returns:
        list: A list of dictionaries with 'role' and 'content' keys
    """
    # Split the input string by 'Bot:' or 'Me:'
    turns = []
    current_parts = input_string.split('Bot:')[1:] + input_string.split('Me:')[1:]
    
    # Process Bot: turns
    for part in input_string.split('Bot:')[1:]:
        turns.append({
            'role': 'assistant',
            'content': part.split('Me:')[0].strip()
        })
    
    # Process Me: turns
    for part in input_string.split('Me:')[1:]:
        turns.append({
            'role': 'user',
            'content': part.split('Bot:')[0].strip()
        })
    
    # Sort the turns based on their original order
    return sorted(turns, key=lambda x: input_string.index(x['content']))

if __name__ == "__main__":


    for i in range(1,11):
        with open("appendices\\Appendix_6\\p" + str(i) + "_run.json", "r") as file:
            data = json.load(file)
            messages = parse_conversation(data["0"]["LLM_INSTRUCTION"])
            messages.remove(messages[-1])
            print(messages)
            print("-"*50 + "\n\n")