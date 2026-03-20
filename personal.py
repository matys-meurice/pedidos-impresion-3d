import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

def enviar_email(destino, pedido, precio, id):
    user = os.getenv("EMAIL_USER") or st.secrets["EMAIL_USER"]
    password = os.getenv("EMAIL_PASS") or st.secrets["EMAIL_PASS"]

    link = f"https://pedidos-impresion-3d-confirmar.streamlit.app"

    mensaje = f"""
    Tu pedido:
    {pedido}

    Precio: {precio} €

    Confirma aquí tu id es {id}:
    {link}
    """

    msg = MIMEText(mensaje)
    msg['Subject'] = 'Confirmación impresión 3D'
    msg['From'] = user
    msg['To'] = destino

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(user, password)
            server.send_message(msg)
        print("Email enviado")
    except Exception as e:
        print("Error enviando email:", e)

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
            fecha = st.date_input(f"Fecha de entrega {todo['id']}", key=f"Fecha{todo['id']}")

            if st.button(f"Enviar presupuesto {todo['id']}"):
                supabase.table("todos").update({
                    "precio": precio,
                    "fecha": fecha,
                    "estado": "presupuesto"
                }).eq("id", todo["id"]).execute()

                enviar_email(
                    todo["email"],
                    todo["pedido"],
                    precio,
                    todo["id"]
                )

                st.success("Presupuesto enviado y email enviado")


        # SI ESTA CONFIRMADO → poner en impresión
        if todo["estado"] == "confirmado":
            st.write(f"Nombre: (todo['nombre'])")
            st.write(f"Lugar de entrega: (todo['lugar'])")
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