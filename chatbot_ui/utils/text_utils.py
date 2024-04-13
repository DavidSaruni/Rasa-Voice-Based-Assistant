def dictionary_value_to_string(data) -> str:
    # Extract 'text' values and filter out None values
    text_values = [item['text'] for item in data if 'text' in item and item['text']]

    # Join 'text' values into a single sentence using a space separator
    text_sentence = ' '.join(text_values)
    return text_sentence
    
