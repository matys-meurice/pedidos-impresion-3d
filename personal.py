import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText


def enviar_email(destino, pedido, precio, id):
    user = st.secrets["EMAIL_USER"]
    password = st.secrets["EMAIL_PASS"]

    link = f"https://pedidos-impresion-3d-confirmar.streamlit.app/"

    mensaje = f"""
Tu pedido:
{pedido}

Precio: {precio} €

Confirma aquí:
{link}
"""

    msg = MIMEText(mensaje)
    msg['Subject'] = 'Confirmación impresión 3D'
    msg['From'] = user
    msg['To'] = destino

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

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

opcion = st.radio(
    "Ver pedidos:",
    ["Pendientes", "Confirmados", "Imprimiendo", "Por entregar"]
)

load_dotenv()

url = os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
key = os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

def get_todos(estado):
    response = supabase.table('todos').select('*').eq('estado', estado).execute()
    return response.data

st.title("Panel de pedidos")

if opcion == "Pendientes":
    estado_filtrado = "pendiente"
elif opcion == "Confirmados":
    estado_filtrado = "confirmado"
elif opcion == "Imprimiendo":
    estado_filtrado = "imprimiendo"
elif opcion == "Por entregar":
    estado_filtrado = "por entregar"

todos = get_todos(estado_filtrado)

if todos:    
    for todo in todos:
        st.write("------")
        st.write(f"ID: {todo['id']}")
        st.write(f"Modelo: {todo['pedido']}")

        # PENDIENTE → poner precio
        if todo["estado"] == "pendiente":
            precio = st.number_input(
                f"Precio ID {todo['id']}",
                key=f"precio_{todo['id']}"
            )

            fecha = st.date_input(
                f"Fecha de entrega {todo['id']}",
                key=f"fecha_{todo['id']}"
            )

            if st.button(f"Enviar presupuesto {todo['id']}"):

                if precio <= 0:
                    st.error("Pon un precio válido")
                    st.stop()

                supabase.table("todos").update({
                    "precio": float(precio),
                    "fecha": str(fecha),
                    "estado": "presupuesto"
                }).eq("id", todo["id"]).execute()

                enviar_email(
                    todo["email"],
                    todo["pedido"],
                    precio,
                    todo["id"]
                )


        # CONFIRMADO → pasar a imprimiendo
        if todo["estado"] == "confirmado":
            st.write(f"Nombre: {todo.get('nombre', 'Sin nombre')}")
            st.write(f"Fecha de entrga: {todo.get('fecha')}")

            if st.button(f"Marcar imprimiendo {todo['id']}"):
                supabase.table("todos").update({
                    "estado": "imprimiendo"
                }).eq("id", todo["id"]).execute()
                st.rerun()

        # IMPRIMIENDO → por entregar
        if todo["estado"] == "imprimiendo":
            st.write(f"Nombre: {todo.get('nombre', 'Sin nombre')}")
            st.write(f"Fecha de entrga: {todo.get('fecha')}")

            if st.button(f"Marcar por entregar {todo['id']}"):
                supabase.table("todos").update({
                    "estado": "por entregar"
                }).eq("id", todo["id"]).execute()
                st.rerun()


        # Por entregar → eliminar
        if todo["estado"] == "por entregar":
            st.write(f"Nombre: {todo.get('nombre', 'Sin nombre')}")
            st.write(f"Fecha de entrga: {todo.get('fecha')}")
            if st.button(f"Eliminar (entregado) {todo['id']}"):
                supabase.table("todos").delete().eq("id", todo["id"]).execute()
                st.rerun()



else:
    st.write("No hay pedidos")