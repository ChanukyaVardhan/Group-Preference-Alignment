
from openai import OpenAI
import pandas as pd
import ast
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

#read csv file
#get group, question, options
# Group = ['Less than $30,000']
# Question = "How much, if at all, do you worry about the following happening to you? Being the victim of a terrorist attack"
# Options = "['Worry a lot', 'Worry a little', 'Do not worry at all', 'Refused']"

# Example CSV read logic (pseudo-code)
# import pandas as pd
df = pd.read_csv("fintrain_data.csv")


# Prepare a list to store the results
openai_responses = []

group_intepretation_map = {
    "Democrat": "Consider yourself as a United States citizen. In today's United States politics, you are Democrat.",
    "Republican": "Consider yourself as a United States citizen. In today's United States politics, you are Republican.",
    "$100,000 or more": "Consider yourself as a United States citizen. Your total family annual income from all sources before taxes is $100,000 or more.",
    "Less than $30,000": "Consider yourself as a United States citizen. Your total family annual income from all sources before taxes is less than $30,000."
}

for index, row in df.iterrows():
# for index, row in df.head(20).iterrows():
    Group, Question, Options = row['group'], row['question'], row['references']
    Options_list = ast.literal_eval(Options)

    # # Static example for demonstration
    # Group = 'Democrat'
    # Question = "How much, if at all, do you worry about the following happening to you? Being the victim of a terrorist attack"
    # Options = "['Worry a lot', 'Worry a little', 'Do not worry at all', 'Refused']"

    # system_prompt = (
    #     "Generate more descriptive options for each of the standard response options to a survey question assuming you are a member of the group. "
    #     "The options should reflect the perspective of the specified group, considering their unique concerns and life experiences."
    # )
    # user_prompt = f"Group: {Group}. Question: {Question}. Here are the standard response options: {Options}. Provide a more descriptive option for each."
    
    system_prompt = f"""
        {group_intepretation_map[Group]} 
        Generate more descriptive options for each of the standard response options to a survey question, in first person perspective.
        The options should reflect your perspective, considering your concerns and life experiences."
    """
    reference_description_format = ", ".join([f'reference_description_{idx+1}' for idx in range(len(Options_list))])
    user_prompt = f"""Question: {Question}. Here are the standard response options: {Options}. Provide a more descriptive option for each without including the option in the description.
    The output format should be:"[{reference_description_format}]."
    """
    # Give the descriptions in new lines without any list format. Do not enumerate the descriptions as a list.
    # "['reference_description_1', 'reference_description_2', 'reference_description_3', ..., 'reference_description_n'], where n is {len(Options_list)}."

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )
    generated_content = completion.choices[0].message.content
    # print(completion.choices[0].message.content)
    openai_responses.append(generated_content)
    
    # generated_content_list = ast.literal_eval(generated_content)
    
    # print(len(Options_list) == len(generated_content_list))

with open('options_list.txt', 'w') as file:
    for option in openai_responses:
        file.write(option + '\n\n\n')

df['openai'] = openai_responses
#df.loc[df.index < 20, 'openai'] = openai_responses
df.to_csv('openai_data.csv', index=False)



