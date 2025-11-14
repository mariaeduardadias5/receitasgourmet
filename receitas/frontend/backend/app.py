from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from models import get_conn, init_db

app = Flask(__name__)
CORS(app)

# Inicializa o banco
init_db()

@app.route("/api/cadastrar", methods=["POST"])
def cadastrar_usuario():
    data = request.json
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not nome or not email or not senha:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    conn = get_conn()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                  (nome, email, senha))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"erro": "E-mail já cadastrado"}), 400

    conn.close()
    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201


@app.route("/api/login", methods=["POST"])
def login_usuario():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = c.fetchone()
    conn.close()

    if not usuario:
        return jsonify({"erro": "E-mail ou senha incorretos"}), 401

    return jsonify({
        "id": usuario["id"],
        "nome": usuario["nome"],
        "email": usuario["email"]
    })


# ===============================
# ROTAS DE RECEITAS
# ===============================

@app.route("/api/receitas", methods=["GET", "POST"])
def receitas():
    if request.method == "POST":
        data = request.json
        nome = data.get("nome")
        ingredientes = data.get("ingredientes")
        preparo = data.get("preparo")
        tempo = data.get("tempo")
        autor_id = data.get("autor_id")

        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO receitas (nome, ingredientes, preparo, tempo, autor_id)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, ingredientes, preparo, tempo, autor_id))
        conn.commit()
        conn.close()

        return jsonify({"mensagem": "Receita adicionada com sucesso!"}), 201

    else:
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT r.*, u.nome as autor
            FROM receitas r
            LEFT JOIN usuarios u ON r.autor_id = u.id
        """)
        receitas = [dict(row) for row in c.fetchall()]
        conn.close()
        return jsonify(receitas)


@app.route("/api/receitas/<int:id>", methods=["PUT", "DELETE"])
def receita_por_id(id):
    if request.method == "PUT":
        data = request.json
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            UPDATE receitas SET nome=?, ingredientes=?, preparo=?, tempo=?
            WHERE id=?
        """, (data.get("nome"), data.get("ingredientes"), data.get("preparo"), data.get("tempo"), id))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Receita atualizada!"})

    if request.method == "DELETE":
        conn = get_conn()
        c = conn.cursor()
        c.execute("DELETE FROM receitas WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Receita excluída!"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
