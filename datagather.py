label_set = ['Democrat', 'Republican', '$100,000 or more', 'Less than $30,000', 'Overall']


#first get list of all questions

#first get responses of this to question id
import pandas as pd
import ast
from io import StringIO
df = pd.read_csv('/scratch/sca321/drl/Group-Preference-Alignment/OQA_data/OpinionsQA/human_resp/Pew_American_Trends_Panel_disagreement_500/info.csv')  # Replace with your file path
extracted_data = df[['key', 'question', 'references']].copy()
print(extracted_data)

df2 = pd.read_csv('/scratch/sca321/drl/Group-Preference-Alignment/OQA_data/distributions/Pew_American_Trends_Panel_disagreement_500_default_human.csv')
answered_data = df2[['qkey', 'group', 'attribute', 'D_H']].copy()
print(answered_data)

joined_data = pd.merge(extracted_data, answered_data, left_on='key', right_on='qkey')
print(joined_data)


joined_data.to_csv('join_data.csv', index=False)


# Function to parse the list and select the corresponding answer
def get_answer(row):
    # Convert string list in 'D_H' column to actual list
    D_H_list = ast.literal_eval(row['D_H'])
    # Convert string list in 'references' column to actual list
    references_list = ast.literal_eval(row['references'])
    # Find the index of the maximum value in 'D_H_list'
    max_index = D_H_list.index(max(D_H_list))
    # Return the corresponding answer from 'references_list'
    return references_list[max_index]

# Apply the function to each row and create the 'answer' column
joined_data['answer'] = joined_data.apply(get_answer, axis=1)
print(df)
#filter for our labels
filtered_df = joined_data[joined_data['group'].isin(label_set)]
filtered_df.to_csv('mytrain_data.csv', index=False)

df = filtered_df
# Step 1: Create a DataFrame of 'Overall' answers
overall_answers = df[df['group'] == 'Overall'][['key', 'answer']]
# Step 2: Merge the 'Overall' answers back to the original DataFrame on 'key'
df = df.merge(overall_answers, on='key', suffixes=('', '_overall'))
# Step 3: Create the 'neutral' column
df['neutral'] = df.apply(lambda row: '' if row['group'] == 'Overall' else row['answer_overall'], axis=1)
# Drop the temporary 'answer_overall' column as it's no longer needed after creating 'neutral'
df.drop('answer_overall', axis=1, inplace=True)
# Display the DataFrame to verify the new 'neutral' column
#print(df.head())

df.rename(columns={'neutral': 'answer', 'answer': 'correction'}, inplace=True)

# Step 2: Remove rows with group "Overall"
df = df[df['group'] != 'Overall']

# Step 3: Select only the specified columns
final_df = df[['key', 'question', 'group', 'answer', 'correction', 'references']]

# Display the final DataFrame to verify
print(final_df.head())

final_df.to_csv('fintrain_data.csv', index=False)








