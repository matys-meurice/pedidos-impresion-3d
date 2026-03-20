import streamlit as st
from supabase import create_client, Client
import os

# 🔹 Conexión a Supabase
url = os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
key = os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Confirmar pedido")

# 🔹 Pide el ID manualmente
id_input = st.text_input("Introduce el ID del pedido")

if id_input:
    try:
        pedido_id = int(id_input)
    except ValueError:
        st.error("ID no válido. Debe ser un número.")
        st.stop()

    # 🔹 Obtener datos del pedido
    response = supabase.table("todos").select("*").eq("id", pedido_id).execute()
    if response.data:
        pedido = response.data[0]
        st.write(f"**Modelo:** {pedido['pedido']}")
        st.write(f"**Precio:** {pedido.get('precio', 'N/A')} €")
        st.write(f"**Fecha de entrega(en el patio):** {pedido.get('Fecha')}")
        st.write(f"**Estado actual:** {pedido.get('estado', 'pendiente')}")

        # 🔹 Pide nombre y lugar de entrega
        nombre = st.text_input("Tu nombre")
        lugar = st.text_input("Lugar de entrega (clase, patio, calistenia, etc.)")

        if st.button("Confirmar pedido"):
            if not nombre or not lugar:
                st.error("Debes poner tu nombre y lugar de entrega")
            else:
                # 🔹 Actualizar pedido en Supabase
                supabase.table("todos").update({
                    "estado": "confirmado",
                    "nombre": nombre,
                    "lugar": lugar
                }).eq("id", pedido_id).execute()

                st.success("Pedido confirmado ")
    else:
        st.error("Pedido no encontrado")
else:
    st.info("Introduce un ID para continuar")