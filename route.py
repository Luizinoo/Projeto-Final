from bottle import Bottle, request, redirect, static_file, template, response, run
from app.controllers.application import Application

app = Bottle()
ctl = Application()

# Rota para exibir notícias
@app.route('/noticias')
def noticias():
    return ctl.noticias()

# Rota para adicionar uma nova notícia
@app.route('/add_noticia', method='POST')
def add_noticia():
    title = request.forms.get('title')
    content = request.forms.get('content')
    upload = request.files.get('upload')
    
    file_path = None
    if upload:
        file_path = f"app/static/uploads/{upload.filename}"
        upload.save(file_path)
    
    ctl.add_news(title, content, file_path)
    return redirect('/noticias')

# Rota para baixar arquivos
@app.route('/download/<filename>')
def download(filename):
    return static_file(filename, root='app/static/uploads', download=filename)

# Home
@app.route('/')
def home():
    return ctl.home()

# Editar
@app.route('/edit')
def edit():
    return ctl.edit()

# Exibição de membros
@app.route('/membros')
def membros():
    current_user = request.get_cookie('session_id', secret='sua-chave-secreta')
    if not current_user:
        return redirect('/login')
    return ctl.membros()

# Rota de login
@app.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return ctl.process_login()
    return ctl.login()

# Criar
@app.route('/create')
def create():
    return ctl.create()

# Confirmar
@app.route('/confirma')
def confirma():
    return ctl.confirma()

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

# Rota para editar produtos
@app.route('/edit_product', method='POST')
def edit_product():
    old_name = request.forms.get('old_name')
    new_name = request.forms.get('new_name')
    quantity = int(request.forms.get('quantity'))
    ctl.edit_product(old_name, new_name, quantity)
    return redirect('/membros')

# Rota para remover produtos
@app.route('/remove_product', method='POST')
def remove_product():
    name = request.forms.get('name')
    ctl.remove_product(name)
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
