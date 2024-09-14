from app.models.user_account import UserAccount, SuperAccount
from app.models.product import Product
import json
import uuid


class UserRecord():
    def __init__(self):
        self.__allusers= {'user_accounts': [], 'super_accounts': []}
        self.__authenticated_users = {}
        self.read('user_accounts')
        self.read('super_accounts')
        self.read_products()
        self.__product = []

    # Funções para usuários
    def read(self,database):
        account_class = SuperAccount if (database == 'super_accounts' ) else UserAccount
        try:
            with open(f"app/controllers/db/{database}.json", "r") as fjson:
                user_d = json.load(fjson)
                self.__allusers[database]= [account_class(**data) for data in user_d]
        except FileNotFoundError:
            self.__allusers[database].append(account_class('Guest', '000000'))

    def __write(self,database):
        try:
            with open(f"app/controllers/db/{database}.json", "w") as fjson:
                user_data = [vars(user_account) for user_account in \
                self.__allusers[database]]
                json.dump(user_data, fjson)
                print(f'Arquivo gravado com sucesso (Usuário)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Usuário)!')

    def setUser(self,username,password):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if username == user.username:
                    user.password= password
                    print(f'O usuário {username} foi editado com sucesso.')
                    self.__write(account_type)
                    return username
        print('O método setUser foi chamado, porém sem sucesso.')
        return None

    def removeUser(self, user):
        for account_type in ['user_accounts', 'super_accounts']:
            if user in self.__allusers[account_type]:
                print(f'O usuário {"(super) " if account_type == "super_accounts" else ""}{user.username} foi encontrado no cadastro.')
                self.__allusers[account_type].remove(user)
                print(f'O usuário {"(super) " if account_type == "super_accounts" else ""}{user.username} foi removido do cadastro.')
                self.__write(account_type)
                return user.username
        print(f'O usuário {user.username} não foi identificado!')
        return None

    def book(self, username, password, permissions):
        account_type = 'super_accounts' if permissions else 'user_accounts'
        account_class = SuperAccount if permissions else UserAccount
        new_user = account_class(username, password, permissions) if permissions else account_class(username, password)
        self.__allusers[account_type].append(new_user)
        self.__write(account_type)
        return new_user.username

    def getUserAccounts(self):
        return self.__allusers['user_accounts']


    def getCurrentUser(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None


    def getAuthenticatedUsers(self):
        return self.__authenticated_users


    def checkUser(self, username, password):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if user.username == username and user.password == password:
                    session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                    self.__authenticated_users[session_id] = user
                    return session_id  # Retorna o ID de sessão para o usuário
        return None


    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id] # Remove o usuário logado

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

    def add_product(self, name, quantity):
        new_product = Product(name, int(quantity))  # Certifique-se de que a quantidade seja um inteiro
        self.__product.append(new_product)
        self.__write_products()


    def get_products(self):
        return self.__product

    def remove_product(self, name):
        self.__product = [p for p in self.__product if p.name != name]
        self.__write_products()

    def get_product_by_name(self, name):
        for product in self.__product:
            if product.name == name:
                return product
        return None

    def update_product(self, old_name, new_name, quant):
        product = self.get_product_by_name(old_name)
        if product:
            product.name = new_name
            product.quantity = int(quant)  # Converter a quantidade para inteiro
            self.__write_products()

    # Método para obter um usuário pelo nome
    def get_user_by_username(self, username):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if user.username == username:
                    return user
        return None
