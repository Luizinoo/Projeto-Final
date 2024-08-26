from app.controllers.application import Application
from bottle import Bottle, static_file, run


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/membros', methods=['GET'])
@app.route('/membros/<username>', methods=['GET'])
def action_pagina(username=None):
    if not username:
        return ctl.render('membros')
    else:
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
        redirect(f'/pagina/{username}')
    else:
        return redirect('/login')

#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='localhost', port=8080, debug=True)