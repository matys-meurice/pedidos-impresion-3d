import streamlit as st
from supabase import create_client, Client
import os

# 🔹 Conexión a Supabase
url = os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
key = os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Confirmar pedido")

# 🔹 Input ID
id_input = st.text_input("Introduce el ID del pedido")

if id_input:
    try:
        pedido_id = int(id_input)
    except ValueError:
        st.error("ID no válido. Debe ser un número.")
        st.stop()

    # 🔹 Obtener pedido
    response = supabase.table("todos").select("*").eq("id", pedido_id).execute()

    if response.data:
        pedido = response.data[0]

        #  SI YA ESTÁ CONFIRMADO
        if pedido.get("estado") == "confirmado":
            st.success("Este pedido ya ha sido confirmado")

            st.write(f"**Modelo:** {pedido['pedido']}")
            st.write(f"**Precio:** {pedido.get('precio', 'N/A')} €")
            st.write(f"**Fecha de entrega:** {pedido.get('fecha', 'No definida')}")
            st.write(f"**Lugar:** En el patio en las barras de calistenia.")
            st.write(f"**Nombre:** {pedido.get('nombre', 'No definido')}")

            st.info("Se entregará en el patio en la fecha indicada.")
            st.stop()
        elif pedido.get("estado") == "pendiente":
            st.write(f"**El pedido ahun no ha sido revisado recibira un mail pronto**")

        #  MOSTRAR DATOS SI NO CONFIRMADO
        st.write(f"**Modelo:** {pedido['pedido']}")
        st.write(f"**Precio:** {pedido.get('precio', 'N/A')} €")
        st.write(f"**Fecha de entrega (en el patio):** {pedido.get('fecha', 'No definida')}")
        st.write(f"**Estado actual:** {pedido.get('estado', 'pendiente')}")

        # 🔹 Formulario de confirmación
        nombre = st.text_input("Tu nombre")
        if st.button("Confirmar pedido"):
            if not nombre:
                st.error("Debes poner tu nombre y lugar de entrega")
            else:
                supabase.table("todos").update({
                    "estado": "confirmado",
                    "nombre": nombre,
                }).eq("id", pedido_id).execute()

                st.success("Pedido confirmado correctamente 🎉")
                st.rerun()

    else:
        st.error("Pedido no encontrado")

else:
    st.info("Introduce un ID para continuar")