#python sql/database.py
#python -c "import sqlite3; conn = sqlite3.connect('sql/estoque.db'); c = conn.cursor(); c.execute('SELECT * FROM produtos'); print(c.fetchall())"
import sqlite3
def criar_banco():
    conexao = sqlite3.connect('sql/estoque.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT  NOT NULL UNIQUE,
        classe TEXT NOT NULL,
        embalagem TEXT NOT NULL
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contagens(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data DATE
    )
''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens_contagem(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contagem_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (contagem_id) REFERENCES contagens(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')

    conexao.commit()
    conexao.close()
criar_banco()