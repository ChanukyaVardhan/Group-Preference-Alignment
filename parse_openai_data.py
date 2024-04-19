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
        openai_responses = ast.literal_eval(openai_row)

        # Find the index of the column_name in references (e.g., 'answer' or 'correction')
        idx = references.index(row[column_name])

        if len(references)!=len(openai_responses):
            # print(row)
            # return references[idx]
            return pd.NA

        # Return the corresponding openai response
        return openai_responses[idx]
    except Exception as e:
        if "Perhaps you forgot a comma?" in str(e):            
            openai_row = row["openai"]
            if "." == openai_row[-1]:
                openai_row = openai_row[:-1]
            formatted_str = re.sub(r"^\['", '["', openai_row)  # Replace the starting '[' with [" correctly
            formatted_str = re.sub(r"'\]$", '"]', formatted_str)  # Replace the ending ']' with "]"
            formatted_str = re.sub(r"', \n'", '","', formatted_str)  # Replace inner ', \n' delimiters
            formatted_str = re.sub(r"',\n'", '","', formatted_str)  # Replace inner ',\n' delimiters
            formatted_str = re.sub(r"', '", '","', formatted_str)  # Replace inner ', ' delimiters
            
            openai_responses = ast.literal_eval(formatted_str)
            idx = references.index(row[column_name])

            return openai_responses[idx]
        elif "unterminated string literal" in str(e):
            openai_row = row["openai"]
            if "." == openai_row[-1]:
                openai_row = openai_row[:-1]
            # print(openai_row, "\n\n\n\n\n")
            formatted_str = re.sub(r"^\['", '["', openai_row)  # Replace the starting '[' with [" correctly
            formatted_str = re.sub(r"'\]$", '"]', formatted_str)  # Replace the ending ']' with "]"
            formatted_str = re.sub(r"', \n'", '","', formatted_str)  # Replace inner ', \n' delimiters
            formatted_str = re.sub(r"',\n'", '","', formatted_str)  # Replace inner ',\n' delimiters
            formatted_str = re.sub(r"', '", '","', formatted_str)  # Replace inner ', ' delimiters

            # formatted_str = str([formatted_str]) # Doesn't Work
            openai_responses = ast.literal_eval(formatted_str)
            idx = references.index(row[column_name])

            return openai_responses[idx]
        elif '"\n"' in row["openai"] or '" \n"' in row["openai"]:
            openai_row = row["openai"]
            if "." == openai_row[-1]:
                openai_row = openai_row[:-1]

            formatted_str = re.sub(r'" \n"', '", "', openai_row)
            formatted_str = re.sub(r'"\n"', '", "', formatted_str)

            openai_responses = ast.literal_eval(formatted_str)
            idx = references.index(row[column_name])

            return openai_responses[idx]
        elif row["openai"].count('["') > 1 and row["openai"].count('"]') > 1:
            openai_row = row["openai"]
            if "." == openai_row[-1]:
                openai_row = openai_row[:-1]
            openai_row = openai_row.replace('["', '"').replace('"]', '",')
            openai_row = '[' + openai_row.strip() + ']'

            openai_responses = ast.literal_eval(openai_row)
            idx = references.index(row[column_name])

            return openai_responses[idx]
        elif row['key'] in ["EVOTHREE_W34", "ELECT_CONF3_PRVSUP_W92"]:
            return pd.NA
        else:
            print(str(e))
            print(row)
            openai_row = row["openai"]
            if "." == openai_row[-1]:
                openai_row = openai_row[:-1]
            # print(openai_row)

            openai_responses = ast.literal_eval(openai_row)
            idx = references.index(row[column_name])

            print(openai_responses)
            print(idx)

            print('not founddd')

        return pd.NA

# Apply the function to each row for the 'answer' and 'correction' columns
df['openai_answer'] = df.apply(get_openai_response, column_name='answer', axis=1)
df['openai_correction'] = df.apply(get_openai_response, column_name='correction', axis=1)

# Filter out rows where 'openai_answer' or 'openai_correction' is empty
df = df.dropna(subset=['openai_answer', 'openai_correction'])

# Select and rename specific columns
df = df[['key', 'question', 'group', 'openai_answer', 'openai_correction']]
df.rename(columns={'openai_answer': 'answer', 'openai_correction': 'correction'}, inplace=True)

# Save the updated DataFrame back to CSV
df.to_csv('openai_alignerdata.csv', index=False)
