from app.models.user_account import UserAccount
from app.models.product import Product
from app.controllers.datarecord import DataRecord
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
            'cadastro': self.cadastro,
            'confirma': self.confirma,
            'noticias': self.noticias,
            'produtos': self.produtos,
            'serviços': self.serviços
        }

        self.__model = DataRecord()
        self.__current_loginusername = None

        self.product = None
        self.edited = None
        self.removed = None
        self.created = None

    def render(self, page, parameter=None):
        content = self.pages.get(page)
        if not parameter:
            return content()
        else:
            return content(parameter)

    def get_session_id(self):
        return request.get_cookie('session_id')

    def home(self):
        return template('app/views/html/home')

    def confirma(self):
        return template('app/views/html/confirma')

    def login(self):
        return template('app/views/html/login')

    def membros(self, username=None):
        session_id = self.get_session_id()
        if username and session_id:
            if self.__model.get_user_name(session_id) == username:
                user = self.__model.get_current_user(session_id)
                return template('app/views/html/membros', transfered=True, current_user=user)
            else:
                return template('app/views/html/membros', transfered=False)
        else:
            return template('app/views/html/membros', transfered=False)

    def is_authenticated(self, username):
        session_id = self.get_session_id()
        current_user = self.__model.get_user_name(session_id)
        return username == current_user

    def authenticate_user(self, username, password):
        self.logout_user()
        session_id = self.__model.check_user(username, password)
        if session_id:
            self.__current_loginusername = username
            return session_id, username
        return None

    def logout_user(self):
        self.__current_loginusername = None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)
            response.delete_cookie('session_id')

    def administracao(self):
        return template('app/views/html/administracao')

    def cadastro(self):
        return template('app/views/html/cadastro')

    def produto(self):
        return template('app/views/html/produto')

    def delete(self):
        current_user = self.get_current_user_by_session_id()
        if current_user:
            self.delete_user()

    def noticias(self):
        return template('app/views/html/noticias')

    def produtos(self):
        products = self.__model.get_products()
        return template('app/views/html/produtos', products=products)

    def serviços(self):
        return template('app/views/html/serviços')

    def insert_user(self, username, password):
        self.created = self.__model.book_user(username, password)
        redirect('/confirma')

    def update_user(self, username, password):
        self.edited = self.__model.set_user(username, password)
        redirect('/login')

    def edit(self):
        current_user = self.get_current_user_by_session_id()
        return template('app/views/html/edit', current_user=current_user)

    def get_current_user_by_session_id(self):
        session_id = self.get_session_id()
        return self.__model.get_current_user(session_id)

    def delete_user(self):
        current_user = self.get_current_user_by_session_id()
        self.logout_user()
        self.removed = self.__model.remove_user(current_user)
        redirect('/home')

    def add_product(self, product_name, quant):
        self.__model.add_product(product_name, quant)
        redirect('/produtos')

    def upload_photo(self):
        upload = request.files.get('photo')
        if upload:
            upload_dir = 'app/static/img/profiles'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            file_path = os.path.join(upload_dir, upload.filename)
            upload.save(file_path)
            
            session_id = self.get_session_id()
            user = self.__model.get_current_user(session_id)
            if user:
                user.profile_image = file_path
                self.__model.update_user_profile_image(user)
        
        redirect('/membros')

    def serve_profile_image(self, filename):
        return static_file(filename, root='app/static/img/profiles')
