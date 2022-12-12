import openai as ai
from typing import Union

AGE_THRESHOLD = 15

def get_api_from_a_file(filename):
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)
        return ''
ai.api_key = get_api_from_a_file('.\\other\\apiKey.txt') # you have to create apiKey.txt in 'other' folder


def generate_summarization_for_prompt(interests: str):
    model_response = ai.Completion.create(model="text-davinci-003", prompt= \
        f"""Task: convert description of interests into given format:
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


def handle_occasion(text: str, occasion: str):
    return text + f' on {occasion}'


def make_prompt_data_for_gpt(interests: str, gender: str, age: int, occasion: str):
    class prompt_data:
        interests: str
        gender: str
        age: int
        occasion: str
    prompt_data.interests = generate_summarization_for_prompt(interests)
    prompt_data.gender = handle_gender(gender, age)
    prompt_data.age = age
    prompt_data.occasion = occasion
    return prompt_data


def generate_text_with_model(prompt_data):
    response = ai.Completion.create(model="text-davinci-003", prompt= \
        f"""Task: based on description of interests, gender, age, occasion find what gift would suit to certain person.
        Find exactly one gift idea.

        Interests of person 1: (playing football, watching football matches)
        Gender of person 1: (Man)
        Age of person 1: (11)
        Occasion: ({prompt_data.occasion})
        Gift for person 1: (ball)
        <end>
        Interests of person 2: (painting, drawing)
        Gender of person 2: (Non-binary)
        Age of person 2: (25)
        Occasion: ({prompt_data.occasion})
        Gift for person 2: (set of brushes)
        <end>
        Interests of person 3: (playing computer games, watching films)
        Gender of person 3: (Woman)
        Age of person 3: (16)
        Occasion: ({prompt_data.occasion})
        Gift for person 3: (computer mouse)
        <end>
        Interests of person 4: ({prompt_data.interests})
        Gender of person 4: ({prompt_data.gender})
        Age of person 4: ({str(prompt_data.age)})
        Occasion: ({prompt_data.occasion})
        Gift for person 4:""" , temperature=0.5).choices[0].text
    beg = response.rindex("(")
    end = response.rindex(")")
    return response[beg+1:end]


class TextGenerator:
    def __init__(self):
        self.is_done = False

    def generate_text(self, interests: str, gender: str, age: Union[str, int], occasion: str):
        age = int(age)
        prompt_data = make_prompt_data_for_gpt(interests, gender, age, occasion)
        model_output = generate_text_with_model(prompt_data)
        self.is_done = True
        return model_output
