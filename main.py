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
    "Especificaciones (si no especifica bien despues no nos hacemos responsables)",
    help="Ej: tamaño(no obigatorio), color, como es (de los personalizados)..."
)

st.text("""Consulta el catalogo en:
        

        """)

if st.button("Pedir"):
    if pedido and email:
        response = supabase.table('todos').insert({
            'pedido': pedido,
            'email': email,
            'especificaciones': especificaciones,
            'estado': 'pendiente'
        }).execute()

        pedido_id = response.data[0]['id']
        
        st.success(f"""¡Ya has pedido!  
            El id de su pedido es {pedido_id}  
            Para ver el estado de su pedido mire en:

            https://pedidos-impresion-3d-confirmar.streamlit.app/
            """)
    else:
        st.error("Rellena todo")