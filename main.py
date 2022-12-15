import streamlit as st
import pandas as pd
import numpy as np
import re

from generating.text_generation import TextGenerator
from generating.image_generation import ImageGenerator
from generating.text_generation import make_prompt_data_for_gpt

def gift_idea_to_amazon(idea: str):
    idea_to_url = idea.lower().strip().replace(" ", "+")
    url = f"https://www.amazon.com/s?k={idea_to_url}"

    return url

def update_image(interests: str, gender: str, age: str, occasion: str, gift_ideas, index):
    img_gen = ImageGenerator()

    prompt_data = make_prompt_data_for_gpt(
            interests, gender, int(age), occasion)

    if isinstance(gift_ideas, list):
        output_image = img_gen.generate_image(gift_ideas[index], prompt_data)
    else:
        output_image = img_gen.generate_image('burning computer', prompt_data)

    return output_image


def generate_text_and_image(interests: str, gender: str, age: str, occasion: str):
    img_gen = ImageGenerator()
    text_gen = TextGenerator()

    output_text = text_gen.generate_text(interests, gender, age, occasion)
    gift_ideas = [idea for idea in re.split('[0-9]|\.', output_text.replace("\n", "")) if idea]

    prompt_data = make_prompt_data_for_gpt(
            interests, gender, int(age), occasion)

    output_image = img_gen.generate_image(gift_ideas[0], prompt_data)

    if text_gen.is_done and img_gen.is_done:
        return gift_ideas, output_image
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
            'Describe the person interests', placeholder='swimming, car racing', max_chars=2000)

        if 'is_generated' not in st.session_state:
            st.session_state.is_generated = False
        
        should_generate = sel_col.button('Generate')

        should_update = disp_col.button('Need another idea?')

        if 'count' not in st.session_state:
            st.session_state.count = 0

        if should_generate:
            st.session_state.is_generated = True
            st.session_state.ideas, output_image = generate_text_and_image(interests, gender, age, occasion)
            disp_col.write(f'What about... {st.session_state.ideas[0].upper()}?')
            disp_col.image(output_image)
        
        if should_update:
            if st.session_state.is_generated:
                st.session_state.count += 1
                if st.session_state.count < 3:
                    output_image = update_image(interests, gender, age, occasion, st.session_state.ideas, st.session_state.count)
                    disp_col.write(f'What about... {st.session_state.ideas[st.session_state.count].upper()}?')
                    disp_col.image(output_image)
                else: 
                    output_image = update_image(interests, gender, age, occasion, 'sad face', st.session_state.count)
                    disp_col.write(f'I have run out of ideas :(')
                    disp_col.image(output_image)
            else:
                disp_col.write(f'Consider generating some ideas first :)')