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

st.set_page_config(page_title="Produtos", layout="wide")

with open(os.path.join(ASSETS_PATH, "styles.css")) as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.logo(image="assets/logo.png", link="https://github.com/rosaldo")

st.write("# Produtos")

def load_data():
    products = dbase.session.query(dbase.products).all()
    return pd.DataFrame([{
        "id": product.id,
        "Nome": product.name,
        "Codigo_barras": product.bar_code,
        "Descricao": product.description,
        "Fornecedor": product.supplier_id,
        "Em_estoque": product.stock,
        "Unidade": product.unit,
        "Preco": product.price,
        "Margem": product.margin,
        "Ativo": product.active,
        "Criado_em": product.created_at,
        "Atualizado_em": product.updated_at
    } for product in products])

df_products = load_data()

def save_data(row):
    product = dbase.session.query(dbase.products).filter(dbase.products.id == int(row.id)).first()
    if product:
        product.name = row.Nome
        product.bar_code = row.Codigo_barras
        product.description = row.Descricao
        product.supplier_id = row.Fornecedor
        product.stock = row.Em_estoque
        product.unit = row.Unidade
        product.price = row.Preco
        product.margin = row.Margem
        product.active = bool(row.Ativo)
        product.updated_at = dtt.now()
        dbase.session.commit()
        st.rerun()

with st.form("add_product", clear_on_submit=True):
    name, bar_code, description, supplier, stock, unit, price, margin, add_button = st.columns(9)
    name_input = name.text_input("Nome", key="Nome", placeholder="Nome")
    bar_code_input = bar_code.text_input("Codigo de barras", key="Codigo_barras", placeholder="Codigo de barras")
    description_input = description.text_input("Descricao", key="Descricao", placeholder="Descricao")
    supplier_input = supplier.selectbox("Fornecedor", dbase.session.query(dbase.suppliers).all(), key="Fornecedor", placeholder="Fornecedor")
    stock_input = stock.number_input("Em estoque", key="Em_estoque", placeholder="Em estoque")
    unit_input = unit.text_input("Unidade", key="Unidade", placeholder="Unidade")
    price_input = price.number_input("Preco", key="Preco", placeholder="Preco")
    margin_input = margin.number_input("Margem", key="Margem", placeholder="Margem")
    add_button.markdown("<div style='padding: 14px'>", unsafe_allow_html=True)
    add_product = add_button.form_submit_button("Adicionar Produto", use_container_width=True)
    add_button.markdown("</div>", unsafe_allow_html=True)

if add_product and name_input and bar_code_input and description_input and stock_input and unit_input and price_input and margin_input:
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
gb.configure_column("Criado_em", editable=False, cellStyle={"textAlign": "center"}, sorted=True, sort="desc")
gb.configure_column("Atualizado_em", editable=False, cellStyle={"textAlign": "center"})
gb.configure_column("Em_estoque", cellDataType="number")
gb.configure_column("Preco", cellDataType="number")
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
