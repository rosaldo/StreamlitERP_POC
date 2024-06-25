import os

import pandas as pd
import streamlit as st

<<<<<<< HEAD
version_global = "1.8.0"
=======
version_global = "1.7.0"
>>>>>>> 4d7587dfb47fa1aa10f4f2b8e4a7c9c54e5697eb
version = "1.0.0"
ASSETS_PATH = "assets"

st.set_page_config(page_title="Home")

with open(os.path.join(ASSETS_PATH, "styles.css")) as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.logo(image="assets/logo.png", link="https://github.com/rosaldo")

st.write("# Home")