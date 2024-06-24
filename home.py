import os

import pandas as pd
import streamlit as st

version_global = "1.3.0"
version = "1.0.0"
ASSETS_PATH = "assets"

st.set_page_config(page_title="Home")

with open(os.path.join(ASSETS_PATH, "styles.css")) as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.logo(image="assets/logo.png", link="https://github.com/rosaldo")

st.write("# Home")