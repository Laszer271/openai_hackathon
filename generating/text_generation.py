from typing import Union

AGE_THRESHOLD = 15


def generate_summarization_for_prompt(interests: str):
    if len(interests) > 50:
        return interests[:50]
    return interests

def handle_gender_and_age(text: str, gender: str, age: int):
    text += f' for a {age} years old'
    if age > AGE_THRESHOLD:
        if gender != 'Non-binary':
            text += ' ' + gender.lower()
    else:
        if gender == 'Woman':
            text += ' girl'
        elif gender == 'Man':
            text += ' boy'
    return text


def handle_occasion(text: str, occasion: str):
    return text + f' on {occasion}'


def make_prompt_for_gpt(interests: str, gender: str, age: int, occasion: str):
    prompt = generate_summarization_for_prompt(interests)
    prompt = handle_gender_and_age(prompt, gender, age)
    prompt = handle_occasion(prompt, occasion)
    return prompt


def generate_text_with_model(prompt):
    # here a GPT model should be called
    return prompt


class TextGenerator:
    def __init__(self):
        self.is_done = False

    def generate_text(self, interests: str, gender: str, age: Union[str, int], occasion: str):
        age = int(age)
        prompt = make_prompt_for_gpt(interests, gender, age, occasion)
        model_output = generate_text_with_model(prompt)

        self.is_done = True
        return model_output
