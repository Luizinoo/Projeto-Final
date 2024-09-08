from app.controllers.application import Application
from bottle import Bottle, static_file, run, request, response, redirect


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route("/")
def inicio():
    redirect ('/home')


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')


@app.route('/home', method='GET')
def home():
    return ctl.render('home')


@app.route('/membros/<username>', methods=['GET'])
def action_pagina(username=None):
    return ctl.render('membros',username)


@app.route('/login', method='GET')
def login():
    return ctl.render('login')


@app.route('/login', method='POST')
def action_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, username= ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, \
        secure=True, max_age=3600)
        redirect(f'/membros/{username}')
    else:
        return redirect('/login')


@app.route('/cadastro', method='GET')
def create_getter():
    return ctl.render('cadastro')


@app.route('/confirma', method='GET')
def confirma():
    return ctl.render('confirma')


@app.route('/cadastro', method='POST')
def cadastro_action():
    username = request.forms.get('username')
    password = request.forms.get('password')
    ctl.insert_user(username, password)
    return ctl.render('confirma')


@app.route('/edit', method='GET')
def edit_getter():
    return ctl.render('edit')


@app.route('/edit', method='POST')
def edit_action():
    username = request.forms.get('username')
    password = request.forms.get('password')
    ctl.update_user(username, password)
    return ctl.render('edit')


@app.route('/delete', method='POST')
def delete_action():
    ctl.delete_user()
    return ctl.render('login')


@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    redirect('/login')


@app.route('/administracao', method='GET')
def administracao():
    return ctl.render('administracao')


@app.route('/cadastro', method='GET')
def cadastro():
    return ctl.render('cadastro')


@app.route('/noticias', method='GET')
def noticias():
    return ctl.render('noticias')


@app.route('/produtos', method='GET')
def produtos():
    return ctl.render('produtos')


@app.route('/serviços', method='GET')
def serviços():
    return ctl.render('serviços')

#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='localhost', port=8080, debug=True)