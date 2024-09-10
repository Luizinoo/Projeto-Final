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
    product_name = request.forms.get('product')
    quant = request.forms.get('quant')
    ctl.add_product(product_name, quant)
    return redirect('/produtos')

@app.route('/serviços', method='GET')
def serviços():
    return ctl.render('serviços')

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)