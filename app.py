from flask import Flask,jsonify,json,request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from flask_jwt_extended import JWTManager
app.config["JWT_SECRET_KEY"] = "abc"
jwt = JWTManager(app)
@app.route("/api/cafeinas/id/<int:id>",methods=["GET"])
def pegar(id):
    import sqlite3
    conn = sqlite3.connect("cafeinas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM cafeina WHERE id = ?",(id,))
    cafeinas = cursor.fetchall()
    cursor.close()
    conn.close()
    if cafeinas == []:
        return jsonify({"erro":"id nao encontrado"})
    return jsonify({"nome":cafeinas}),200

@app.route("/api/cafeinas",methods=["POST"])
def adicionar():
    data = request.json
    import sqlite3
    conn = sqlite3.connect("cafeinas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cafeina (nome,nivel_de_cafeina) VALUES (?,?)",(data["nome"],data["tipo"]))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem":"Cafeina registrada"}),201

@app.route("/api/cafeinas/<int:id>",methods=["DELETE"])
def deletar(id):
    import sqlite3 
    conn = sqlite3.connect("cafeinas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cafeina WHERE id = ?",(id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem":"deletado"}),201

@app.route("/api/cafeinas/<int:id>",methods=["PUT"])
def atualizar(id):
    data = request.json
    import sqlite3 
    conn = sqlite3.connect("cafeinas.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE cafeina nome = ?, tipo = ?, WHERE id = ?",(data["nome"],data["tipo"],id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem":"dados atualizados"}),201

@app.route("/api/cafeinas/nivel/<nivel_de_cafeina>",methods=["GET"])
def pegar_nivel(nivel_de_cafeina):
    if nivel_de_cafeina not in ["muitobaixa","baixa","média","alta","muitoalta"]:
        return jsonify({"erro":"dados invalidos"}),400
    import sqlite3 
    conn = sqlite3.connect("cafeinas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM cafeina WHERE nivel_de_cafeina = ?",(nivel_de_cafeina,))
    nomes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"mensagem":nomes}),201

@app.route("/api/usuarios/cadastro",methods=["POST"])
def adicionar_usuario():
    data = request.json
    import sqlite3 
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    from werkzeug.security import generate_password_hash
    senha_hash = generate_password_hash(data["senha"])
    cursor.execute("INSERT INTO usuario (usuario,senha) VALUES (?,?)",(data["usuario"],senha_hash))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensagem":"dados atualizados"}),201
@app.route("/api/usuarios/login",methods=["POST"])
def logar_usuario():
    data = request.json
    import sqlite3 
    from werkzeug.security import check_password_hash
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    for conta in resultado:
        if (conta[1]) == (data["usuario"]):
            if check_password_hash(conta[2], data["senha"]):
                from flask_jwt_extended import create_access_token
                token = create_access_token(identity=conta[0])
                return jsonify({"mensagem":"login efetuado com sucesso","token":token}),200
            else:
                return jsonify({"erro":"senha incorreta"}),400
        else:
            return jsonify({"erro":"usuario não existente"}),400
    return jsonify({"erro":"erro(possivelmente é no banco de dados)"}),403


app.run(debug=True)