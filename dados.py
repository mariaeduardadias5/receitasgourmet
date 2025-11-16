import sqlite3

conn = sqlite3.connect("receitas.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()

print("\n=== Usuários ===")
for row in c.execute("SELECT * FROM usuarios"):
    print(dict(row))

print("\n=== Receitas ===")
for row in c.execute("SELECT * FROM receitas"):
    print(dict(row))

conn.close()
