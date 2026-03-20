import streamlit as st
from supabase import create_client, client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: client = create_client(url, key)

def add_todo(pedido):
    supabase.table('todos').insert({'pedido': pedido}).execute()

st.title("Pedir impresiones 3D")

email = st.text_input("Tu email")
pedido = st.text_input("URL del modelo")

if st.button("Pedir"):
    if pedido and email:
        supabase.table('todos').insert({
            'pedido': pedido,
            'email': email,
            'estado': 'pendiente'
        }).execute()
        st.success("¡Ya has pedido!")
    else:
        st.error("Rellena todo")