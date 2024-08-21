from app.controllers.application import Application
from bottle import Bottle, static_file


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:



#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='localhost', port=8080, debug=True)