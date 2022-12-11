from typing import Union
from PIL import Image

AGE_THRESHOLD = 15


def generate_summarization_for_prompt(text: str):
    if len(text) > 50:
        return text[:50]
    return text


def handle_occasion(text: str, occasion: str):
    prefix = 'a' if occasion.lower()[0] in ['a', 'e', 'i', 'o', 'u'] else 'an'
    return text + f' as {prefix} {occasion} gift'


def make_prompt_for_dalle(text: str, occasion: str):
    prompt = generate_summarization_for_prompt(text)
    prompt = handle_occasion(prompt, occasion)
    return prompt


def generate_image_with_model(prompt):
    # here a GPT model should be called
    placeholder = Image.open('other/christmass_tree.jpeg')

    return placeholder


class ImageGenerator:
    def __init__(self):
        self.is_done = False

    def generate_image(self, text: str, occasion: str):
        prompt = make_prompt_for_dalle(text, occasion)
        model_output = generate_image_with_model(prompt)

        self.is_done = True
        return model_output
