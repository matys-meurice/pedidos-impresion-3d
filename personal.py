import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

# comprobar contraseña
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")

    st.stop()

load_dotenv()

url = os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
key = os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

def get_todos():
    response = supabase.table('todos').select('*').execute()
    return response.data

st.title("Panel de pedidos")

todos = get_todos()

if todos:
    for todo in todos:
        st.write("------")
        st.write(f"ID: {todo['id']}")
        st.write(f"Modelo: {todo['pedido']}")
        st.write(f"Estado: {todo['estado']}")

        # SI ESTA PENDIENTE → poner precio
        if todo["estado"] == "pendiente":
            precio = st.number_input(f"Precio ID {todo['id']}", key=f"precio_{todo['id']}")

            if st.button(f"Enviar presupuesto {todo['id']}"):
                supabase.table("todos").update({
                    "precio": precio,
                    "estado": "presupuesto"
                }).eq("id", todo["id"]).execute()

        # SI ESTA CONFIRMADO → poner en impresión
        if todo["estado"] == "confirmado":
            if st.button(f"Marcar imprimiendo {todo['id']}"):
                supabase.table("todos").update({
                    "estado": "imprimiendo"
                }).eq("id", todo["id"]).execute()

        # SI ESTA IMPRIMIENDO → borrar al terminar
        if todo["estado"] == "imprimiendo":
            if st.button(f"Eliminar {todo['id']}"):
                supabase.table("todos").delete().eq("id", todo["id"]).execute()
                st.rerun()

else:
    st.write("No hay pedidos")