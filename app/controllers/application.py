from app.controllers.datarecord import DataRecord
from bottle import template, redirect, request, response


class Application():

    def __init__(self):

        self.pages = {
            'home' : self.home,
            'membros': self.membros,
            'login': self.login,
            'administracao' : self.administracao,
            'cadastro' : self.cadastro,
            'noticias' : self.noticias,
            'produtos' : self.produtos,
            'serviços' : self.serviços
        }

        self.__model= DataRecord()
        self.__current_loginusername= None


    def render(self,page,parameter=None):
        content = self.pages.get(page)
        if not parameter:
            return content()
        else:
            return content(parameter)


    def get_session_id(self):
        return request.get_cookie('session_id')


    def home(self):
        return template('app/views/html/home')

    def login(self):
        return template('app/views/html/login')


    def membros(self,username=None):
        session_id = self.get_session_id()
        if username and session_id:
            print('Entrei aqui com session_id = ' + session_id + ' e username = ' + username)
            if self.__model.getUserName(session_id) == username:
                user = self.__model.getCurrentUser(session_id)
                return template('app/views/html/membros', \
                transfered=True, current_user=user)
            else:
                return template('app/views/html/membros', \
                transfered=False)
        else:
            return template('app/views/html/membros', \
            transfered=False)


    def is_authenticated(self, username):
        session_id = self.get_session_id()
        current_user = self.__model.getUserName(session_id)
        if username == current_user:
            return True
        else:
            return False


    def authenticate_user(self, username, password):
        self.logout_user()
        session_id = self.__model.checkUser(username, password)
        if session_id:
            self.__current_username= self.__model.getUserName(session_id)
            return session_id, username
        return None


    def logout_user(self):
        self.__current_username= None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)

    def administracao(self):
        return template('app/views/html/administracao')

    def cadastro(self):
        return template('app/views/html/cadastro')

    def noticias(self):
        return template('app/views/html/noticias')

    def produtos(self):
        return template('app/views/html/produtos')

    def serviços(self):
        return template('app/views/html/serviços')