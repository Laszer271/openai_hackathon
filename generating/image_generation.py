from typing import Union
from PIL import Image
import io
import requests
import openai

AGE_THRESHOLD = 15


def generate_summarization_for_prompt(text: str):
    if len(text) > 50:
        return text[:50]
    return text


# def handle_occasion(text: str, occasion: str):
#     prefix = 'a' if occasion.lower()[0] in ['a', 'e', 'i', 'o', 'u'] else 'an'
#     return text + f' as {prefix} {occasion} gift'


def make_prompt_for_dalle(text: str, prompt_data):
    #prompt = generate_summarization_for_prompt(text)
    #prompt = handle_occasion(prompt, occasion)

    prompt = f"an abstract watercolor painting of {prompt_data.age} year old {prompt_data.gender} with a {text}"

    return prompt


def generate_image_with_model(prompt):
    # here a GPT model should be called
    placeholder = Image.open('other/christmass_tree.jpeg')

    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256"
    )
    image_url = response['data'][0]['url']

    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))

    return img


class ImageGenerator:
    def __init__(self):
        self.is_done = False

    def generate_image(self, text: str, prompt_data):
        prompt = make_prompt_for_dalle(text, prompt_data)
        model_output = generate_image_with_model(prompt)

        self.is_done = True
        return model_output
