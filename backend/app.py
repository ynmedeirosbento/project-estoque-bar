#python backend/app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/cadastrar-produto', methods=['POST'])
def cadastrar_produto():
    nome = request.json.get('nome')
    classe = request.json.get('classe')
    embalagem = request.json.get('embalagem')
    conexao = sqlite3.connect('sql/estoque.db')
    cursor = conexao.cursor()
    cursor.execute('INSERT INTO produtos(nome, classe, embalagem) VALUES (?, ?, ?)', (nome, classe, embalagem))
    conexao.commit()
    conexao.close()
    return jsonify({'mensagem': 'Produto cadastrado com sucesso!'})

@app.route('/nova-contagem', methods=['POST'])
def nova_contagem():
    nome = request.json.get('nome')
    
    conexao = sqlite3.connect('sql/estoque.db')
    cursor = conexao.cursor()
    
    cursor.execute('INSERT INTO contagens (nome, data) VALUES (?, DATE("now"))', (nome,))
    contagem_id = cursor.lastrowid

    cursor.execute('SELECT id FROM produtos')
    produtos = cursor.fetchall()

    for produto in produtos:
        cursor.execute('INSERT INTO itens_contagem(contagem_id, produto_id, quantidade) VALUES (?, ?, 0)',
        (contagem_id, produto[0]))
    
    conexao.commit()
    conexao.close()

    return jsonify({'contagem_id': contagem_id})

@app.route('/contagem/<int:contagem_id>')
def contagem(contagem_id):
    conexao = sqlite3.connect('sql/estoque.db')
    cursor = conexao.cursor()
    cursor.execute('''
        SELECT p.nome, p.classe, p.embalagem, i.quantidade, i.id
        FROM itens_contagem i
        JOIN produtos p ON i.produto_id = p.id
        WHERE i.contagem_id = ?
    ''', (contagem_id,))
    cursor.execute('SELECT nome, data FROM contagens WHERE id = ?', (contagem_id,))
    info = cursor.fetchone()
    itens = cursor.fetchall()
    conexao.close()
    return render_template('contagem.html', itens=itens, contagem_id=contagem_id, nome=info[0], data=info[1])

@app.route('/atualizar-quantidade', methods=['POST'])
def atualizar_quantidade():
    item_id = request.json.get('item_id')
    quantidade = request.json.get('quantidade')
    conexao = sqlite3.connect('sql/estoque.db')
    cursor = conexao.cursor()
    cursor.execute('UPDATE itens_contagem SET quantidade = ? WHERE id = ?', (quantidade, item_id))
    conexao.commit()
    conexao.close()
    return jsonify({'mensagem': 'Quantidade atualizada!'})

@app.route('/historico')
def historico():
    conexao = sqlite3.connect('sql/estoque.db')
    cursor = conexao.cursor()
    
    cursor.execute('SELECT id, nome, data FROM contagens ORDER BY data DESC')
    contagens = cursor.fetchall()
    conexao.close()
    
    return render_template('historico.html', contagens=contagens)
    
@app.route('/comparar/<int:id1>/<int:id2>')
def comparar(id1, id2):
    conexao = sqlite3.connect('sql/estoque.db')
    cursor = conexao.cursor()

    cursor.execute('SELECT nome FROM contagens WHERE id = ?', (id1,))
    nome1 = cursor.fetchone()[0]

    cursor.execute('SELECT nome FROM contagens WHERE id = ?', (id2,))
    nome2 = cursor.fetchone()[0]

    cursor.execute('''
        SELECT p.nome, i.quantidade
        FROM itens_contagem i
        JOIN produtos p ON i.produto_id = p.id
        WHERE i.contagem_id = ?
    ''', (id1,))
    itens1 = dict(cursor.fetchall())

    cursor.execute('''
        SELECT p.nome, i.quantidade
        FROM itens_contagem i
        JOIN produtos p ON i.produto_id = p.id
        WHERE i.contagem_id = ?
    ''', (id2,))
    itens2 = dict(cursor.fetchall())

    conexao.close()

    return render_template('comparar.html', 
                         nome1=nome1, nome2=nome2,
                         itens1=itens1, itens2=itens2)

@app.route ('/excluir-contagem', methods=['POST'])
def excluir_contagem ():
    id = request.json.get('id')

    conexao = sqlite3.connect('sql/estoque.db')
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM itens_contagem WHERE contagem_id = ?', (id,))
    cursor.execute('DELETE FROM contagens WHERE id = ?', (id,))

    conexao.commit()
    conexao.close()

    return jsonify({'mensagem': 'Contagem excluída!'})

@app.route ('/excluir-item', methods=['POST'])
def excluir_item ():
    id = request.json.get('id')

    conexao = sqlite3.connect('sql/estoque.db')
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM itens_contagem WHERE  id = ?', (id,))

    conexao.commit()
    conexao.close()

    return jsonify ({'mensagem': 'Iten excluído com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0')