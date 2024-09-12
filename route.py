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

# Exibir produtos
@app.route('/produtos')
def produtos():
    return ctl.produtos()

# Editar produto
@app.route('/edit_product')
def edit_product():
    return ctl.edit_product()

# Exibir serviços com produtos
@app.route('/servicos')
def servicos():
    products = ctl.get_products()  # Garantir que a função retorna uma lista
    return template('app/views/html/servicos.html', products=products)

# Revisão do carrinho
@app.route('/review_cart')
def review_cart():
    return ctl.review_cart()

# Checkout com geração de nota e atualização do estoque
@app.route('/checkout', method=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        invoice_data = ctl.generate_invoice()
        if invoice_data:
            ctl.update_inventory(invoice_data)
        return template('app/views/html/checkout.html', invoice_data=invoice_data)
    return template('app/views/html/checkout.html', invoice_data=None)

# Download da nota
@app.route('/download-invoice/<invoice_id>', method='GET')
def download_invoice(invoice_id):
    file_path = f'app/static/invoices/{invoice_id}.pdf'
    return static_file(file_path, root='app/static/invoices', download=f"{invoice_id}.pdf")

# Rota para adicionar produtos
@app.route('/add_product', method='POST')
def add_product():
    name = request.forms.get('name')
    price = float(request.forms.get('price'))
    quantity = int(request.forms.get('quantity'))
    ctl.add_product(name, price, quantity)
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

# Adicionar ao carrinho
@app.route('/add_to_cart', method='POST')
def add_to_cart():
    ctl.add_to_cart()
    return redirect('/review_cart')

# Logout
@app.route('/logout')
def logout():
    response.delete_cookie('session_id')
    return redirect('/login')

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
