from flask import Flask, render_template, session, request, redirect, url_for, flash
import database
import sqlite3

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'

# Função para criar a tabela de usuários no banco de dados
def create_users_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

create_users_table()

# Rota para a página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Se o método for POST, processa o formulário de registro
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not (email and password):
            flash('Preencha todos os campos!', 'error')
        else:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
    # Se o método for GET, exibe a página de registro
    return render_template('register.html')


# Rota para a página de login
# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            flash('Login realizado com sucesso!', 'success')
            session['user_id'] = user[0]  # Definindo o ID do usuário na sessão
            # Redirecionar para a página do sistema de produtos após o login bem-sucedido
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos!', 'error')

    # Se o método for GET ou se o login falhar, exiba a página de login
    return render_template('login.html')

# Rota para a página do sistema de produtos
@app.route('/home')
def index():
    # Verificar se o usuário está autenticado
    if 'user_id' not in session:
        # Se o usuário não estiver autenticado, redirecione para a página de login
        return redirect(url_for('login'))

    # Se o usuário estiver autenticado, continue com a lógica para carregar a página inicial
    products = database.fetch_products()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    id = request.form['id']
    name = request.form['name']
    stock = request.form['stock']

    if not (id and name and stock):
        flash('Preencha todos os campos!', 'error')
    elif database.id_exists(id):
        flash('ID já existe!', 'error')
    else:
        try:
            stock_value = int(stock)
            database.insert_product(id, name, stock_value)
            flash('Produto adicionado com sucesso!', 'success')
        except ValueError:
            flash('O estoque precisa ser um número inteiro.', 'error')
    return redirect(url_for('index'))

@app.route('/update_product/<id>', methods=['POST'])
def update_product(id):
    name = request.form.get('name')
    stock = request.form.get('stock')

    if name is not None or stock is not None:
        database.update_product(id, name, stock)
        flash('Produto atualizado com sucesso!', 'success')
    else:
        flash('Nada a ser atualizado!', 'warning')

    return redirect(url_for('index'))

@app.route('/delete_product/<id>', methods=['GET'])
def delete_product(id):
    database.delete_product(id)
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
