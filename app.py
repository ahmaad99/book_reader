import openai
import csv
from tqdm import tqdm
from dotenv import load_dotenv
import streamlit as st
import os
# Set your OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
word = st.text_input("Enter a word or expression:")

execute = st.button("Execute")


if execute:

    with open('add_word.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        # # Write the header row
        # writer.writerow(['word', 'meaning', 'sentence1', 'sentence2',
        #                 'sentence3', 'sentence4', 'sentence5'])

        messages1 = [
            {"role": "system", "content": "You are an intelligent assistant."},
            {"role": "user", "content": f"Write only the meaning of the word '{word}' don't mention the word itself"}]

        messages2 = [
            {"role": "system", "content": "You are an intelligent assistant."},
            {"role": "user", "content": f"Write 5 sentences with the word '{word}' in a single paragraph  do not index it as 1,2,3,4,5."}
        ]

        try:
            # Make a request to the ChatGPT API
            response1 = openai.Completion.create(
                model="gpt-3.5-turbo",
                messages=messages1,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            response2 = openai.Completion.create(
                model="gpt-3.5-turbo",
                messages=messages2,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Extract the response content
            reply1 = response1.choices[0].message["content"].strip()
            reply2 = response2.choices[0].message["content"].strip()

            sentences = [sentence.strip()
                         for sentence in reply2.split('. ') if sentence]

            while len(sentences) < 5:
                sentences.append('')

            st.write(reply1)
            st.write(sentences)
            writer.writerow([word] + [reply1] + sentences[:5])

        except Exception as e:
            print(f"An error occurred for word '{word}': {e}")
