import os

import pandas as pd
import streamlit as st
from datetime import datetime as dtt
from st_aggrid import (AgGrid, DataReturnMode, GridOptionsBuilder,
                       GridUpdateMode, JsCode)

from aggrid_locale import locale_text
from database import dbase

version = "2.4.0"
ASSETS_PATH = "assets"

st.set_page_config(page_title="Produtos", layout="wide")

with open(os.path.join(ASSETS_PATH, "styles.css")) as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.logo(image="assets/logo.png", link="https://github.com/rosaldo")

st.write("# Produtos")

all_suppliers = dbase.session.query(dbase.suppliers).all()
supplier_names = [supplier.name for supplier in all_suppliers]
supplier_names.insert(0, "Fornecedores")
supplier_dict = {supplier.name: supplier.id for supplier in all_suppliers}
supplier_dict_inv = {supplier.id: supplier.name for supplier in all_suppliers}

def load_data():
    products = dbase.session.query(dbase.products).all()
    return pd.DataFrame([{
        "id": product.id,
        "name": product.name,
        "bar_code": product.bar_code,
        "description": product.description,
        "supplier_id": supplier_dict_inv[product.supplier_id] if product.supplier_id else None,
        "stock": product.stock,
        "unit": product.unit,
        "price": product.price,
        "margin": product.margin,
        "active": product.active,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    } for product in products])

df_products = load_data()

def save_data(row):
    product = dbase.session.query(dbase.products).filter(dbase.products.id == int(row.id)).first()
    if product:
        product.name = row.to_dict()["name"]
        product.bar_code = row.bar_code
        product.description = row.description
        product.supplier_id = supplier_dict[row.supplier_id] if row.supplier_id else None
        product.stock = row.stock
        product.unit = row.unit
        product.price = row.price
        product.margin = row.margin
        product.active = bool(row.active)
        product.updated_at = dtt.now()
        dbase.session.commit()
        st.rerun()

with st.form("add_product", clear_on_submit=True):
    name, bar_code, description, supplier = st.columns(4)
    name_input = name.text_input("Nome", key="name")
    bar_code_input = bar_code.text_input("Codigo de barras", key="bar_code")
    description_input = description.text_input("Descrição", key="description")
    
    supp = supplier.selectbox("Fornecedor", supplier_names, key="supplier_id")
    supplier_input = supplier_dict[supp] if supp != "Fornecedores" else None
    
    stock, unit, price, margin, add_button = st.columns(5)
    stock_input = stock.number_input("Em estoque", key="stock")
    unit_input = unit.text_input("Unidade", key="unit")
    price_input = price.number_input("Preço", key="price")
    margin_input = margin.number_input("Margem", key="margin")
    add_button.markdown("<div style='padding: 14px'>", unsafe_allow_html=True)
    add_product = add_button.form_submit_button("Adicionar Produto", use_container_width=True)
    add_button.markdown("</div>", unsafe_allow_html=True)

if add_product and name_input and bar_code_input and description_input and supplier_input \
    and stock_input and unit_input and price_input and margin_input:
    new_row = dbase.products()
    new_row.name = name_input
    new_row.bar_code = bar_code_input
    new_row.description = description_input
    new_row.supplier_id = supplier_input
    new_row.stock = stock_input
    new_row.unit = unit_input
    new_row.price = price_input
    new_row.margin = margin_input
    dbase.session.add(new_row)
    dbase.session.commit()
    df_products = load_data()

gb = GridOptionsBuilder.from_dataframe(df_products[[col for col in df_products.columns if col.lower() != "id"]])
gb.configure_default_column(editable=True, filter=True, groupable=True)
gb.configure_column("name", "Nome")
gb.configure_column("bar_code", "Código de barras")
gb.configure_column("description", "Descrição")
gb.configure_column("supplier_id", "Fornecedor", cellEditor="agRichSelectCellEditor", cellEditorParams={"values": supplier_names[1:]})
gb.configure_column("stock", "Em estoque", cellDataType="number")
gb.configure_column("unit", "Unidade")
gb.configure_column("price", "Preço", cellDataType="number")
gb.configure_column("margin", "Margem", cellDataType="number")
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
    data=df_products,
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
