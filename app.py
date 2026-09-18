from flask import Flask, render_template, request
from db import get_connection
import psycopg2.extras

app = Flask(__name__)

app.secret_key = "crud-clientes-flask-2026"

@app.route("/")
def index():
    conn = get_connection()

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM clientes ORDER BY id DESC")
        clientes = cur.fetchall()

    conn.close()

    return render_template("index.html", clientes=clientes)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        dpi = request.form["dpi"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]

        conn = get_connection()

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO clientes
                (nombre, dpi, telefono, correo, direccion)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, dpi, telefono, correo, direccion))

        conn.commit()
        conn.close()

        return "Cliente guardado correctamente"

    return render_template("form.html")

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    conn = get_connection()

    if request.method == "POST":
        nombre = request.form["nombre"]
        dpi = request.form["dpi"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]

        with conn.cursor() as cur:
            cur.execute("""
                UPDATE clientes
                SET nombre = %s,
                    dpi = %s,
                    telefono = %s,
                    correo = %s,
                    direccion = %s
                WHERE id = %s
            """, (nombre, dpi, telefono, correo, direccion, id))

        conn.commit()
        conn.close()

        return "Cliente actualizado correctamente"

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM clientes WHERE id = %s", (id,))
        cliente = cur.fetchone()

    conn.close()

    return render_template("form.html", cliente=cliente)

@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
def eliminar_cliente(id):
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM clientes WHERE id = %s",
            (id,)
        )

    conn.commit()
    conn.close()

    return "Cliente eliminado correctamente"

if __name__ == "__main__":
    app.run(debug=True)