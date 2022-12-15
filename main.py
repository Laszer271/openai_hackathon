import streamlit as st
import pandas as pd
import numpy as np

from generating.text_generation import TextGenerator
from generating.image_generation import ImageGenerator
from generating.text_generation import make_prompt_data_for_gpt

def generate_text_and_image(interests: str, gender: str, age: str, occasion: str):
    img_gen = ImageGenerator()
    text_gen = TextGenerator()

    output_text = text_gen.generate_text(interests, gender, age, occasion)
    gift_ideas = [idea for idea in output_text.split("123456789.") if idea]

    prompt_data = make_prompt_data_for_gpt(
            interests, gender, int(age), occasion)

    output_image = img_gen.generate_image(gift_ideas[0], prompt_data)

    if text_gen.is_done and img_gen.is_done:
        return output_text, output_image
    else:
        print(output_image)
        print(output_image)

if __name__ == '__main__':
    model_gui = st.container()

    with model_gui:
        st.header('Gift Picker Assistant')
        st.write('Describe person and occasion for our assistant to help you pick a gift')

        sel_col, disp_col = st.columns(2)

        occasion = sel_col.selectbox('For what occasion is the gift for', options=['Christmas', 'Birthday', 'Other'], index=0)
        age = sel_col.text_input('How old is the person the gift is for', placeholder='15')

        gender = sel_col.selectbox('What is the gender of the person the gift is for',
                              options=['Woman', 'Man', 'Non-binary'], index=0)

        interests = sel_col.text_input(
            'Describe the person interests', placeholder='Likes swimming and car racing', max_chars=2000)

        should_generate = sel_col.button('Generate')

        if should_generate:
            output_text, output_image = generate_text_and_image(interests, gender, age, occasion)
            disp_col.write(output_text)
            disp_col.image(output_image)


