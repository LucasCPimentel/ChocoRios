from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import database

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
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

