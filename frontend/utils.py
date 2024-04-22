import math
import streamlit as st


def display_images(images):
    """ "
    Displays a list of images in a grid
    The images are arranged in rows with two columns per row.
    """

    num_images = len(images)
    rows = []
    num_rows = math.ceil(num_images / 2)

    for i in range(num_rows):
        row = st.columns(2)
        rows.extend(row)

    for j in range(num_images):
        with rows[j].container(height=300):
            st.image(images[j])
