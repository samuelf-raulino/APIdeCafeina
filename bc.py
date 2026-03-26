import sqlite3

conn = sqlite3.connect("usuarios.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE usuario(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario VARCHAR(100),
        senha VARCHAR(100)
)"""
)
conn.commit()
"""
cursor.execute("INSERT INTO cafeina (nome,nivel_de_cafeina) VALUES (?,?)",("Artemis Coffee","baixa"))
conn.commit()
"""
cursor.close()
conn.close()