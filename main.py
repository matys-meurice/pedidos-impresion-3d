import streamlit as st
from supabase import create_client, client
from dotenv import load_dotenv
import os

# Usar Secrets si está en Streamlit Cloud, sino .env en local
url = os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
key = os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]

load_dotenv()

supabase: client = create_client(url, key)

def add_todo(pedido):
    supabase.table('todos').insert({'pedido': pedido}).execute()

st.title("Pedir impresiones 3D")

email = st.text_input("Tu email")
pedido = st.text_input(
    "Modelo (URL o nombre)",
    help="Puedes poner un enlace o un producto del catálogo(nombre)"
)

especificaciones = st.text_input(
    "Especificaciones",
    help="Ej: tamaño(no obigatorio), color, como es (de los personalizados)..."
)
if st.button("Pedir"):
    if pedido and email:
        supabase.table('todos').insert({
            'pedido': pedido,
            'email': email,
            'especificaciones': especificaciones,
            'estado': 'pendiente'
        }).execute()
        st.success(f"¡Ya has pedido!\nEl id de su pedido es {pedido['id']}\nPara ver el estado de su pedido mire en:\nhttps://pedidos-impresion-3d-confirmar.streamlit.app/")
        st.error("Rellena todo")