import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO
import base64
from PIL import Image

from generating.text_generation import TextGenerator
from generating.image_generation import ImageGenerator
from generating.text_generation import make_prompt_data_for_gpt

def gift_idea_to_amazon(idea: str):
    idea_to_url = idea.lower().strip().replace(" ", "+")
    url = f"https://www.amazon.com/s?k={idea_to_url}"

    return url

def update_image(interests: str, gender: str, age: str, gift_ideas, index):
    img_gen = ImageGenerator()

    prompt_data = make_prompt_data_for_gpt(
            interests, gender, int(age))

    if isinstance(gift_ideas, list):
        output_image = img_gen.generate_image(gift_ideas[index], prompt_data)
    else:
        output_image = img_gen.generate_image('burning computer', prompt_data)

    return output_image


def generate_text_and_image(interests: str, gender: str, age: str):
    img_gen = ImageGenerator()
    text_gen = TextGenerator()

    output_text = text_gen.generate_text(interests, gender, age)
    gift_ideas = [idea for idea in re.split('[0-9]|\.', output_text.replace("\n", "")) if idea]

    prompt_data = make_prompt_data_for_gpt(
            interests, gender, int(age))

    output_image = img_gen.generate_image(gift_ideas[0], prompt_data)

    if text_gen.is_done and img_gen.is_done:
        return gift_ideas, output_image
    else:
        print(output_image)
        print(output_image)

def populate_column(img_col, content_col, output_image, cnt):
    # img_col.markdown("<p style = 'text-align: center;'>" + str(img_to_html(output_image))[2:] + "</p> ", unsafe_allow_html=True)
    output_image = output_image.resize((1024, 1024))
    img_col.image(output_image)
    if cnt < N_IDEAS_TO_SHOW:
        content_col.write(f'Idea {st.session_state.count + 1} / {N_IDEAS_TO_SHOW}')
        content_col.write(f'What about... {st.session_state.ideas[cnt].upper()}?')
    else: 
        disp_col.write(f'I have run out of ideas :(')

def image_to_b64(img):
    ret = BytesIO()
    img.save(ret, img.format)
    ret.seek(0)
    return base64.b64encode(ret.getvalue())

def img_to_html(img):
    img = image_to_b64(img)
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(img)
    return img_html

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    N_IDEAS_TO_SHOW = 3
    model_gui = st.container()

    with model_gui:
        st.header('Gift Picker Assistant')
        st.write('Describe person for our assistant to help you pick a gift')

        sel_col, img_col = st.columns(2) # First 2 columns, 1 for input, 2nd for output
        min_col, max_col, disp_col = st.columns([0.5, 0.5, 1]) # Then 4 columns for min/max budget
        sel_col_final, prev_col, next_col = st.columns([1, 0.5, 0.5])  # At the end 3 columns, the first for generate button

        age = sel_col.number_input('How old is the person the gift is for', min_value=0, max_value=200)

        gender = sel_col.selectbox('What is the gender of the person the gift is for',
                              options=['Woman', 'Man', 'Non-binary'], index=0)

        interests = sel_col.text_input(
            'Describe the person interests', placeholder='swimming, car racing', max_chars=2000)

        min_budget = min_col.number_input('Min $', value=10.0, min_value=0.0)
        max_budget = max_col.number_input('Max $', value=50.0, min_value=0.0)

        if 'is_generated' not in st.session_state:
            st.session_state.is_generated = False
        if 'images' not in st.session_state:
            st.session_state.images = []

        should_generate = sel_col_final.button('Generate', key='generate')
        should_update = next_col.button('Show next idea', key='next_idea')
        show_previous = prev_col.button('Show previous idea', key='prev_idea')

        if should_generate:
            st.session_state.count = 0
            st.session_state.is_generated = True
            st.session_state.ideas, output_image = generate_text_and_image(interests, gender, age)
            st.session_state.images.append(output_image)
            populate_column(img_col, disp_col, output_image, 0)
            print('=' * 50)
            print(type(output_image))
            print('=' * 50)

        if show_previous:
            if st.session_state.is_generated:
                if st.session_state.count == 0:
                    output_image = st.session_state.images[st.session_state.count]
                    populate_column(img_col, disp_col, output_image, st.session_state.count)
                    disp_col.write(f'There are no previous ideas, the current one is the first one :)')
                else:
                    st.session_state.count -= 1
                    output_image = st.session_state.images[st.session_state.count]
                    populate_column(img_col, disp_col, output_image, st.session_state.count)
            else:
                disp_col.write(f'Consider generating some ideas first :)')

        if should_update:
            if st.session_state.is_generated:
                st.session_state.count += 1
                if st.session_state.count < len(st.session_state.images):
                    output_image = st.session_state.images[st.session_state.count]
                    populate_column(img_col, disp_col, output_image, st.session_state.count)
                elif st.session_state.count < N_IDEAS_TO_SHOW:
                    output_image = update_image(interests, gender, age, st.session_state.ideas, st.session_state.count)
                    st.session_state.images.append(output_image)
                    populate_column(img_col, disp_col, output_image, st.session_state.count)
                else: 
                    output_image = update_image(interests, gender, age, 'sad face', st.session_state.count)
                    populate_column(img_col, disp_col, output_image, st.session_state.count)
            else:
                disp_col.write(f'Consider generating some ideas first :)')
            st.session_state.count = min(st.session_state.count, N_IDEAS_TO_SHOW)
                    