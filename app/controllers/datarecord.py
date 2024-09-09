from app.models.user_account import UserAccount
from app.models.product import Product
import json
import uuid


class DataRecord:
    def __init__(self):
        self.__product = []
        self.__user_accounts = []
        self.__authenticated_users = {}
        self.read_user_accounts()
        self.read_products()

    # Funções para usuários
    def read_user_accounts(self):
        try:
            with open("app/controllers/db/user_accounts.json", "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount('Guest', '010101', '101010'))

    def __write_user_accounts(self):
        try:
            with open("app/controllers/db/user_accounts.json", "w") as arquivo_json:
                user_data = [vars(user_account) for user_account in self.__user_accounts]
                json.dump(user_data, arquivo_json)
                print(f'Arquivo gravado com sucesso (Usuário)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Usuário)!')

    def set_user(self, username, password):
        for user in self.__user_accounts:
            if username == user.username:
                user.password = password
                print(f'O usuário {username} foi editado com sucesso.')
                self.__write_user_accounts()
                return username
        else:
            print(f'O usuário {username} não foi identificado!')
            return None

    def remove_user(self, user):
        if user in self.__user_accounts:
            print(f'O usuário {user.username} foi encontrado no cadastro.')
            self.__user_accounts.remove(user)
            print(f'O usuário {user.username} foi removido do cadastro.')
            self.__write_user_accounts()
            return user.username
        print(f'O usuário {user.username} não foi identificado!')
        return None

    def book_user(self, username, password):
        new_user = UserAccount(username, password)
        self.__user_accounts.append(new_user)
        self.__write_user_accounts()
        return new_user.username

    def get_current_user(self, session_id):
        return self.__authenticated_users.get(session_id, None)

    def get_user_name(self, session_id):
        user = self.get_current_user(session_id)
        return user.username if user else None

    def get_user_session_id(self, username):
        for session_id, user in self.__authenticated_users.items():
            if username == user.username:
                return session_id
        return None

    def check_user(self, username, password):
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())
                self.__authenticated_users[session_id] = user
                return session_id
        return None

    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]

    # Funções para produtos
    def read_products(self):
        try:
            with open("app/controllers/db/product.json", "r") as arquivo_json:
                product_data = json.load(arquivo_json)
                self.__product = [Product(**data) for data in product_data]
        except FileNotFoundError:
            self.__product = []

    def __write_products(self):
        try:
            with open("app/controllers/db/product.json", "w") as arquivo_json:
                prod_data = [vars(product) for product in self.__product]
                json.dump(prod_data, arquivo_json)
                print(f'Arquivo gravado com sucesso (Produto)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Produto)!')

    def add_product(self, product_name, quant):
        new_product = Product(product_name, quant)
        self.__product.append(new_product)
        self.__write_products()

    def get_products(self):
        return self.__product
    
    def update_user_profile_image(self, user):
        for existing_user in self.__user_accounts:
            if existing_user.username == user.username:
                existing_user.profile_image = user.profile_image
                self.__write()
                return
        print(f'Usuário {user.username} não encontrado.')
