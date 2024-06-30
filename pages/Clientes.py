import os

import pandas as pd
import streamlit as st
from datetime import datetime as dtt
from st_aggrid import (AgGrid, DataReturnMode, GridOptionsBuilder,
                       GridUpdateMode, JsCode)

from aggrid_locale import locale_text
from database import dbase

version = "3.0.1"
ASSETS_PATH = "assets"

st.set_page_config(page_title="Home", layout="wide")

with open(os.path.join(ASSETS_PATH, "styles.css")) as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.logo(image="assets/logo.png", link="https://github.com/rosaldo")

st.write("# Clientes")

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

with st.form("add_costumer", clear_on_submit=True):
    name, email, address, phone, add_button = st.columns(5)
    name_input = name.text_input("Nome", key="Nome", placeholder="Nome", label_visibility="hidden")
    email_input = email.text_input("Email", key="Email", placeholder="Email", label_visibility="hidden")
    address_input = address.text_input("Endereco", key="Endereco", placeholder="Endereco", label_visibility="hidden")
    phone_input = phone.text_input("Celular", key="Celular", placeholder="Celular", label_visibility="hidden")
    add_button.markdown("<div style='padding-top: 27px'>", unsafe_allow_html=True)
    add_costumer = add_button.form_submit_button("Adicionar Cliente", use_container_width=True)
    add_button.markdown("</div>", unsafe_allow_html=True)

if add_costumer and name_input and email_input and address_input and phone_input:
    new_row = dbase.costumers()
    new_row.name = name_input
    new_row.email = email_input
    new_row.address = address_input
    new_row.phone = phone_input
    dbase.session.add(new_row)
    dbase.session.commit()
    df_costumers = load_data()
    
gb = GridOptionsBuilder.from_dataframe(df_costumers[[col for col in df_costumers.columns if col.lower() != "id"]])
gb.configure_default_column(editable=True, filter=True, groupable=True)
gb.configure_column("Criado_em", editable=False, cellStyle={"textAlign": "center"}, sorted=True, sort="desc")
gb.configure_column("Atualizado_em", editable=False, cellStyle={"textAlign": "center"})
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
    row_id = grid_response["event_data"].get("rowIndex")
    new_row = new_data.iloc[row_id]
    save_data(new_row)
