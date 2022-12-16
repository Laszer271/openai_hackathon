import openai as ai
import streamlit as st
from typing import Union

AGE_THRESHOLD = 15


# def get_api_from_a_file(filename):
#     try:
#         with open(filename, 'r') as f:
#             # It's assumed our file contains a single line,
#             # with our API key

#             return f.read().strip()
#     except FileNotFoundError:
#         print("'%s' file not found" % filename)
#         return ''


# you have to create apiKey.txt in 'other' folder
ai.api_key = st.secrets["api_key"]


def generate_summarization_for_prompt(interests: str):
    model_response = ai.Completion.create(model="text-davinci-003", prompt=f"""Task: convert description of interests into given format:
        Description: (Likes swimming and playing football a lot)
        List: (swimming, playing football)
        <end>
        Description: (playing chess, watching tv)
        List: (playing chess, watching tv)
        <end>
        Description: (adores singing or running)
        List: (singing, running)
        Description: ({interests})
        List: """,
                                          temperature=0.5, stop="\n<end>").choices[0].text
    beg = model_response.rindex("(")
    end = model_response.rindex(")")
    return model_response[beg+1:end]


def handle_gender(gender: str, age: int):
    if age > AGE_THRESHOLD or gender == 'Non-binary':
        return gender
    if gender == 'Woman':
        return 'Girl'
    if gender == 'Man':
        return 'Boy'


# def handle_occasion(text: str, occasion: str):
#     return text + f' on {occasion}'


def make_prompt_data_for_gpt(interests: str, gender: str, age: int):
    class prompt_data:
        interests: str
        gender: str
        age: int
    #prompt_data.interests = generate_summarization_for_prompt(interests)
    prompt_data.interests = interests
    prompt_data.gender = handle_gender(gender, age)
    prompt_data.age = age
    return prompt_data


def generate_text_with_model(prompt_data):
    response = ai.Completion.create(
        model="text-davinci-003", prompt=f"""Please give me a list of ten ideas \
            for gifts for a {prompt_data.age} year old {prompt_data.gender} \
            who is interested in such areas: {prompt_data.interests}. \
            Please be concrete, dont use full sentences. Use a maximum of \
            4 words per idea. Prioritize physical gifts.""", max_tokens=256, temperature=0.5).choices[0].text
    # beg = response.rindex("(")
    # end = response.rindex(")")
    return response


class TextGenerator:
    def __init__(self):
        self.is_done = False

    def generate_text(self, interests: str, gender: str, age: Union[str, int]):
        age = int(age)
        prompt_data = make_prompt_data_for_gpt(
            interests, gender, age)
        model_output = generate_text_with_model(prompt_data)
        self.is_done = True
        return model_output
