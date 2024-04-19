import pandas as pd
import ast
import json
import re

# def safe_parse_list(input_str):
#     try:
#         # Normalize single quotes to double quotes and try to parse
#         return input_str.replace("'", '"')
#     except:
#         # Return empty list if there's an error
#         return []

# Load data from CSV
df = pd.read_csv('openai_data.csv')

# Define a function to process the references and openai columns
def get_openai_response(row, column_name):
    try:
        # Convert the string representations of lists to actual lists
        references = ast.literal_eval(row['references'])

        openai_row = row["openai"]
        if "." == openai_row[-1]:
            openai_row = openai_row[:-1]        
        #openai_row.replace("'", '"')
        openai_responses = ast.literal_eval(openai_row)
        # Using regex to replace only the enclosing single quotes
        # openai_row = re.sub(r"^'|'$", '"', openai_row)  # Replace single quotes at the start and end of the string
        # openai_row = re.sub(r"(?<=\[)'|'(?=\])", '"', openai_row)  # Replace single quotes at the start and end of elements in a list
        #print(openai_row)
        #openai_row = openai_row.replace("'", '"')
        # if len(references)!=len(openai_responses):
        #     print(row)
        
        # Find the index of the column_name in references (e.g., 'answer' or 'correction')
        idx = references.index(row[column_name])
        #print(idx)
        
        # Return the corresponding openai response
        #print(openai_responses[idx])
        return openai_responses[idx]
    except Exception as e:
        print(row)
        openai_row = row["openai"]
        if "." == openai_row[-1]:
            openai_row = openai_row[:-1]    
        formatted_str = re.sub(r"^\['", '["', openai_row)  # Replace the starting '[' with [" correctly
        #print(formatted_str)
        formatted_str = re.sub(r"'\]$", '"]', formatted_str)  # Replace the ending ']' with "]"
        formatted_str = re.sub(r"', '", '","', formatted_str)  # Replace inner ', ' delimiters
        #print(openai_row)
        #openai_responses = ast.literal_eval(formatted_str)
        print(formatted_str)   
        #print(openai_responses) 

        print(references.index(row[column_name]))
        #print(openai_responses[references.index(row[column_name])])
        # In case of any error (e.g., index not found, bad formatting), return NaN
        print('not founddd')
        return pd.NA

# Apply the function to each row for the 'answer' and 'correction' columns
df['openai_answer'] = df.apply(get_openai_response, column_name='answer', axis=1)
df['openai_correction'] = df.apply(get_openai_response, column_name='correction', axis=1)

# Save the updated DataFrame back to CSV
df.to_csv('openao_data_parsed.csv', index=False)
