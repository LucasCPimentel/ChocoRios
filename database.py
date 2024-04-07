import sqlite3


# Função para criar a tabela no banco de dados
def create_table():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id TEXT PRIMARY KEY, name TEXT, stock INTEGER)''')
    conn.commit()
    conn.close()


# Função para inserir um produto no banco de dados
def insert_product(id, name, stock):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO products VALUES (?, ?, ?)", (id, name, stock))
    conn.commit()
    conn.close()


# Função para atualizar um produto no banco de dados
def update_product(id, name=None, stock=None):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    if name is not None:
        c.execute("UPDATE products SET name=? WHERE id=?", (name, id))
    if stock is not None:
        c.execute("UPDATE products SET stock=? WHERE id=?", (stock, id))

    conn.commit()
    conn.close()


# Função para deletar um produto do banco de dados
def delete_product(id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()


# Função para verificar se um ID já existe no banco de dados
def id_exists(id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id=?", (id,))
    result = c.fetchone()
    conn.close()
    return result is not None


# Função para buscar todos os produtos no banco de dados
def fetch_products():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return products

#


# Chamada da função create_table() para garantir que a tabela seja criada
create_table()
