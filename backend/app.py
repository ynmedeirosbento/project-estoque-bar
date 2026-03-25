from flask import Flask, render_template, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_conexao():
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

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
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('INSERT INTO produtos(nome, classe, embalagem) VALUES (%s, %s, %s)', (nome, classe, embalagem))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'mensagem': 'Produto cadastrado com sucesso!'})

@app.route('/nova-contagem', methods=['POST'])
def nova_contagem():
    nome = request.json.get('nome')
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('INSERT INTO contagens (nome, data) VALUES (%s, CURRENT_DATE) RETURNING id', (nome,))
    contagem_id = cursor.fetchone()[0]
    cursor.execute('SELECT id FROM produtos')
    produtos = cursor.fetchall()
    for produto in produtos:
        cursor.execute('INSERT INTO itens_contagem(contagem_id, produto_id, quantidade) VALUES (%s, %s, 0)',
                       (contagem_id, produto[0]))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'contagem_id': contagem_id})

@app.route('/contagem/<int:contagem_id>')
def contagem(contagem_id):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('SELECT nome, data FROM contagens WHERE id = %s', (contagem_id,))
    info = cursor.fetchone()
    cursor.execute('''
        SELECT p.nome, p.classe, p.embalagem, i.quantidade, i.id
        FROM itens_contagem i
        JOIN produtos p ON i.produto_id = p.id
        WHERE i.contagem_id = %s
    ''', (contagem_id,))
    itens = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template('contagem.html', itens=itens, contagem_id=contagem_id, nome=info[0], data=info[1])

@app.route('/atualizar-quantidade', methods=['POST'])
def atualizar_quantidade():
    item_id = request.json.get('item_id')
    quantidade = request.json.get('quantidade')
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('UPDATE itens_contagem SET quantidade = %s WHERE id = %s', (quantidade, item_id))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'mensagem': 'Quantidade atualizada!'})

@app.route('/historico')
def historico():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('SELECT id, nome, data FROM contagens ORDER BY data DESC')
    contagens = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template('historico.html', contagens=contagens)

@app.route('/comparar/<int:id1>/<int:id2>')
def comparar(id1, id2):
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('SELECT nome FROM contagens WHERE id = %s', (id1,))
    nome1 = cursor.fetchone()[0]
    cursor.execute('SELECT nome FROM contagens WHERE id = %s', (id2,))
    nome2 = cursor.fetchone()[0]
    cursor.execute('''
        SELECT p.nome, i.quantidade
        FROM itens_contagem i
        JOIN produtos p ON i.produto_id = p.id
        WHERE i.contagem_id = %s
    ''', (id1,))
    itens1 = dict(cursor.fetchall())
    cursor.execute('''
        SELECT p.nome, i.quantidade
        FROM itens_contagem i
        JOIN produtos p ON i.produto_id = p.id
        WHERE i.contagem_id = %s
    ''', (id2,))
    itens2 = dict(cursor.fetchall())
    cursor.close()
    conexao.close()
    return render_template('comparar.html',
                           nome1=nome1, nome2=nome2,
                           itens1=itens1, itens2=itens2)

@app.route('/excluir-contagem', methods=['POST'])
def excluir_contagem():
    id = request.json.get('id')
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM itens_contagem WHERE contagem_id = %s', (id,))
    cursor.execute('DELETE FROM contagens WHERE id = %s', (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'mensagem': 'Contagem excluída!'})

@app.route('/excluir-item', methods=['POST'])
def excluir_item():
    id = request.json.get('id')
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM itens_contagem WHERE id = %s', (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({'mensagem': 'Item excluído com sucesso!'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')