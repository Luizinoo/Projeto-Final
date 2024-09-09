from app.models.user_account import UserAccount
from app.models.product import Product
from app.controllers.datarecord import UserRecord
from bottle import template, redirect, request, response, static_file
import os

class Application:

    def __init__(self):
        self.pages = {
            'home': self.home,
            'edit': self.edit,
            'membros': self.membros,
            'login': self.login,
            'administracao': self.administracao,
            'create': self.create,
            'confirma': self.confirma,
            'noticias': self.noticias,
            'produtos': self.produtos,
            'serviços': self.serviços
        }

        self.__users = UserRecord()
        self.__current_loginusername = None

        self.product = None
        self.edited = None
        self.removed = None
        self.created = None

    def render(self, page, parameter=None):
        content = self.pages.get(page)
        if not parameter:
            return content()
        return content(parameter)

    def getAuthenticatedUsers(self):
        return self.__users.getAuthenticatedUsers()

    def getCurrentUserBySessionId(self):
        session_id = request.get_cookie('session_id')
        return self.__users.getCurrentUser(session_id)

    def create(self):
        return template('app/views/html/create')

    def delete(self):
        current_user = self.getCurrentUserBySessionId()
        user_accounts= self.__users.getUserAccounts()
        return template('app/views/html/delete', user=current_user, accounts=user_accounts)

    def edit(self):
        current_user = self.getCurrentUserBySessionId()
        user_accounts= self.__users.getUserAccounts()
        return template('app/views/html/edit', user=current_user, accounts= user_accounts)

    def login(self):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            login_render = template('app/views/html/login', \
            username=current_user.username, edited=self.edited, \
            removed=self.removed, created=self.created)
            self.edited = None
            self.removed= None
            self.created= None
            return login_render
        login_render = template('app/views/html/login', username=None, \
        edited=self.edited, removed=self.removed, created=self.created)
        self.edited = None
        self.removed= None
        self.created= None
        return login_render

    def membros(self):
        self.update_users_list()
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            return template('app/views/html/membros', transfered=True, current_user=current_user)
        return template('app/views/html/membros', transfered=False)

    def is_authenticated(self, username):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            return username == current_user.username
        return False

    def authenticate_user(self, username, password):
        session_id = self.__users.checkUser(username, password)
        if session_id:
            self.logout_user()
            response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
            redirect('/membros')
        redirect('/login')

    def delete_user(self):
        current_user = self.getCurrentUserBySessionId()
        self.logout_user()
        self.removed= self.__users.removeUser(current_user)
        self.update_account_list()
        print(f'Valor de retorno de self.removed: {self.removed}')
        redirect('/login')

    def insert_user(self, username, password):
        self.created= self.__users.book(username, password,[])
        print(f'Usuário criado: {self.created}')
        self.update_account_list()
        # redirect('/login')

    def update_user(self, username, password):
        self.edited = self.__users.setUser(username, password)
        redirect('/login')

    def update_users_list(self):
        print('Atualizando a lista de usuários conectados...')
        users = self.__users.getAuthenticatedUsers()
        users_list = [{'username': user.username} for user in users.values()]

    def update_account_list(self):
        print('Atualizando a lista de usuários cadastrados...')
        users = self.__users.getUserAccounts()
        users_list = [{'username': user.username} for user in users]

    def logout_user(self):
        session_id = request.get_cookie('session_id')
        self.__users.logout(session_id)
        response.delete_cookie('session_id')
        self.update_users_list()

    def add_product(self, product_name, quant):
        self.__users.add_product(product_name, quant)
        redirect('/produtos')

    # def upload_photo(self):
    #     upload = request.files.get('photo')
    #     if upload:
    #         upload_dir = 'app/static/img/profiles'
    #         if not os.path.exists(upload_dir):
    #             os.makedirs(upload_dir)
            
    #         file_path = os.path.join(upload_dir, upload.filename)
    #         upload.save(file_path)
            
    #         session_id = self.get_session_id()
    #         user = self.__model.get_current_user(session_id)
    #         if user:
    #             user.profile_image = file_path
    #             self.__model.update_user_profile_image(user)
        
    #     redirect('/membros')

    # def serve_profile_image(self, filename):
    #     return static_file(filename, root='app/static/img/profiles')

    def home(self):
        return template('app/views/html/home')

    def confirma(self):
        return template('app/views/html/confirma')
    
    def administracao(self):
        return template('app/views/html/administracao')

    def produto(self):
        return template('app/views/html/produto')

    def noticias(self):
        return template('app/views/html/noticias')

    def produtos(self):
        products = self.__users.get_products()
        return template('app/views/html/produtos', products=products)

    def serviços(self):
        return template('app/views/html/serviços')