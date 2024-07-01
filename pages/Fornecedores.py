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

st.set_page_config(page_title="Fornecedores", layout="wide")

with open(os.path.join(ASSETS_PATH, "styles.css")) as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.logo(image="assets/logo.png", link="https://github.com/rosaldo")

st.write("# Fornecedores")

def load_data():
    suppliers = dbase.session.query(dbase.suppliers).all()
    return pd.DataFrame([{
        "id": supplier.id,
        "name": supplier.name,
        "email": supplier.email,
        "address": supplier.address,
        "phone": supplier.phone,
        "active": supplier.active,
        "created_at": supplier.created_at,
        "updated_at": supplier.updated_at
    } for supplier in suppliers])

df_suppliers = load_data()

def save_data(row):
    supplier = dbase.session.query(dbase.suppliers).filter(dbase.suppliers.id == int(row.id)).first()
    if supplier:
        supplier.name = row.to_dict()["name"]
        supplier.email = row.email
        supplier.address = row.address
        supplier.phone = row.phone
        supplier.active = bool(row.active)
        supplier.updated_at = dtt.now()
        dbase.session.commit()
        st.rerun()

with st.form("add_supplier", clear_on_submit=True):
    name, email, address, phone, add_button = st.columns(5)
    name_input = name.text_input("Nome", key="name")
    email_input = email.text_input("E-mail", key="email")
    address_input = address.text_input("Endereço", key="address")
    phone_input = phone.text_input("Celular", key="phone")
    add_button.markdown("<div style='padding-top: 28px'>", unsafe_allow_html=True)
    add_supplier = add_button.form_submit_button("Adicionar Fornecedor", use_container_width=True)
    add_button.markdown("</div>", unsafe_allow_html=True)

if add_supplier and name_input and email_input and address_input and phone_input:
    new_row = dbase.suppliers()
    new_row.name = name_input
    new_row.email = email_input
    new_row.address = address_input
    new_row.phone = phone_input
    dbase.session.add(new_row)
    dbase.session.commit()
    df_suppliers = load_data()

gb = GridOptionsBuilder.from_dataframe(df_suppliers[[col for col in df_suppliers.columns if col.lower() != "id"]])
gb.configure_default_column(editable=True, filter=True, groupable=True)
gb.configure_column("name", "Nome")
gb.configure_column("email", "E-mail")
gb.configure_column("address", "Endereço")
gb.configure_column("phone", "Celular", cellStyle={"textAlign": "center"})
gb.configure_column("active", "Ativo", cellStyle={"textAlign": "center"})
gb.configure_column("created_at", "Criado em", editable=False, cellStyle={"textAlign": "center"}, sorted=True, sort="desc")
gb.configure_column("updated_at", "Atualizado em", editable=False, cellStyle={"textAlign": "center"})
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
    data=df_suppliers,
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
