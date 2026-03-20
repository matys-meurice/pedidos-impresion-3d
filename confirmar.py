import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
key = os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

# coger id de la URL
id = st.query_params.get("id")

st.title("Confirmar pedido")

if id:
    # obtener datos del pedido
    response = supabase.table("todos").select("*").eq("id", id).execute()
    pedido = response.data[0]

    st.write(f"Modelo: {pedido['pedido']}")
    st.write(f"Precio: {pedido['precio']} €")

    nombre = st.text_input("Tu nombre")
    lugar = st.text_input("Lugar de entrega (clase, patio, etc.)")

    if st.button("Confirmar pedido"):
        supabase.table("todos").update({
            "estado": "confirmado",
            "nombre": nombre,
            "lugar": lugar
        }).eq("id", id).execute()

        st.success("Pedido confirmado ✅")
else:
    st.error("ID no válido")