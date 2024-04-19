
from openai import OpenAI
import pandas as pd
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

#for index, row in df.iterrows():
for index, row in df.head(5).iterrows():
    Group, Question, Options = row['group'], row['question'], row['references']

    # Static example for demonstration
    Question = "How much, if at all, do you worry about the following happening to you? Being the victim of a terrorist attack"
    Options = "['Worry a lot', 'Worry a little', 'Do not worry at all', 'Refused']"

    system_prompt = (
        "Generate more descriptive options for each of the standard response options to a survey question."
    )

    user_prompt = f"Question: {Question}. Here are the standard response options: {Options}. Provide a more descriptive option for each."

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    generated_content = completion.choices[0].message.content
    print(completion.choices[0].message.content)
    openai_responses.append(generated_content)

    #df['openai'] = completion.choices[0].message.content
df.loc[df.index < 5, 'openai'] = openai_responses
df.to_csv('openai_data.csv', index=False)



