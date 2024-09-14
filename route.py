from app.controllers.application import Application
from bottle import Bottle, static_file, run, request, response, redirect

app = Bottle()
ctl = Application()

#-----------------------------------------------------------------------------
# Rotas:

@app.route("/")
def inicio():
    redirect('/home')

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/home', method='GET')
def home():
    return ctl.render('home')

@app.route('/membros', method='GET')
def membros_getter():
    return ctl.render('membros')

@app.route('/login', method='GET')
def login_getter():
    return ctl.render('login')

@app.route('/edit', method='GET')
def edit_getter():
    return ctl.render('edit')

@app.route('/login', method='POST')
def login_action():
    username = request.forms.get('username')
    password = request.forms.get('password')
    ctl.authenticate_user(username, password)

@app.route('/edit', method='POST')
def edit_action():
    username = request.forms.get('username')
    password = request.forms.get('password')
    print(username + ' sendo atualizado...')
    ctl.update_user(username, password)
    return ctl.render('edit')

@app.route('/create', method='GET')
def create_getter():
    return ctl.render('create')

@app.route('/create', method='POST')
def create_action():
    username = request.forms.get('username')
    password = request.forms.get('password')
    ctl.insert_user(username, password)
    return ctl.render('login')

@app.route('/logout', method='POST')
def logout_action():
    ctl.logout_user()
    return ctl.render('login')

@app.route('/delete', method='GET')
def delete_getter():
    return ctl.render('delete')

@app.route('/delete', method='POST')
def delete_action():
    ctl.delete_user()
    return ctl.render('login')

@app.route('/confirma', method='GET')
def confirma():
    return ctl.render('confirma')

@app.route('/administracao', method='GET')
def administracao():
    return ctl.render('administracao')

@app.route('/noticias', method='GET')
def noticias():
    return ctl.render('noticias')

@app.route('/produtos', method='GET')
def produtos_getter():
    return ctl.render('produtos')

@app.route('/produtos', method='POST')
def produtos_action():
    name = request.forms.get('product')
    quantity = request.forms.get('quant')
    ctl.add_product(name, quantity)
    return redirect('/membros')

@app.route('/delete_product/<name>', method='POST')
def delete_product_action(name):
    ctl.delete_product(name)
    return redirect('/membros')

@app.route('/edit_product/<name>', method='POST')
def edit_product_getter(name):
    return ctl.edit_product(name)

@app.route('/update_product', method='POST')
def update_product_action():
    old_name = request.forms.get('old_name')
    new_name = request.forms.get('new_name')
    quant = request.forms.get('quant')
    ctl.update_product(old_name, new_name, quant)
    return redirect('/membros')

@app.route('/servicos', method='GET')
def servicos_getter():
    return ctl.render('servicos')

@app.route('/comprar_produto', method='POST')
def comprar_produto():
    product_name = request.forms.get('product_name')
    quantity = int(request.forms.get('quantity'))

    # Usar o novo método da classe Application para obter o produto
    product = ctl.get_product_by_name(product_name)
    
    # Converter a quantidade de produto para inteiro, caso seja uma string
    if product and int(product.quantity) >= quantity:
        new_quantity = int(product.quantity) - quantity
        ctl.update_product(product_name, product_name, new_quantity)
        redirect('/servicos')
    else:
        return "Quantidade insuficiente disponível", 400

# Rota para editar a senha de um usuário
@app.route('/admin/edit_user/<username>', method='POST')
def edit_user_password_action(username):
    new_password = request.forms.get('new_password')
    ctl.update_user_password(username, new_password)

# Rota para excluir um usuário
@app.route('/admin/delete_user/<username>', method='POST')
def delete_user_action(username):
    ctl.delete_user_by_admin(username)

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)