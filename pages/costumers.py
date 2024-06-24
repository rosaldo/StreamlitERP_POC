import os

import pandas as pd
import streamlit as st
from datetime import datetime as dtt
from st_aggrid import (AgGrid, DataReturnMode, GridOptionsBuilder,
                       GridUpdateMode, JsCode)

from aggrid_locale import locale_text
from database import dbase

version = "2.0.0"
ASSETS_PATH = "assets"

st.set_page_config(page_title="Home", layout="wide")

with open(os.path.join(ASSETS_PATH, "styles.css")) as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.logo(image="assets/logo.png", link="https://github.com/rosaldo")

st.write("# Costumers")

def load_data():
    costumers = dbase.session.query(dbase.costumers).all()
    return pd.DataFrame([{
        "id": costumer.id,
        "Nome": costumer.name,
        "Email": costumer.email,
        "Endereco": costumer.address,
        "Celular": costumer.phone,
        "Ativo": costumer.active,
        "Criado_em": costumer.created_at,
        "Atualizado_em": costumer.updated_at
    } for costumer in costumers])

df_costumers = load_data()

def save_data(row):
    costumer = dbase.session.query(dbase.costumers).filter(dbase.costumers.id == int(row.id)).first()
    if costumer:
        costumer.name = row.Nome
        costumer.email = row.Email
        costumer.address = row.Endereco
        costumer.phone = row.Celular
        costumer.active = bool(row.Ativo)
        costumer.updated_at = dtt.now()
        dbase.session.commit()
        st.rerun()

if st.button("Add Costumer"):
    new_row = dbase.costumers()
    dbase.session.add(new_row)
    dbase.session.commit()
    df_costumers = load_data()

gb = GridOptionsBuilder.from_dataframe(df_costumers[[col for col in df_costumers.columns if col.lower() != "id"]])
gb.configure_default_column(editable=True, filter=True, groupable=True)
gb.configure_pagination()
gb.configure_grid_options(
    localeText=locale_text,
    autoSizeStrategy={"type":"fitCellContents"},
    enterNavigatesVertically=True,
    enterNavigatesVerticallyAfterEdit=True,
    editType="fullRow",
)

grid_options = gb.build()

grid_response = AgGrid(
    data=df_costumers,
    gridOptions=grid_options,
    height=450,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    allow_unsafe_jscode=True,
    editable=True,
)

if grid_response["event_data"]:
    new_data = pd.DataFrame(grid_response["data"])
    row_id = int(grid_response["event_data"].get("rowIndex"))
    new_row = new_data.iloc[row_id]
    save_data(new_row)
