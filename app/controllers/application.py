from bottle import redirect, request, response, template
from app.models.user_account import UserAccount, SuperAccount
from app.models.product import Product
from app.models.news import News
from app.controllers.datarecord import UserRecord

class Application:
    def __init__(self):
        self.pages = {
            'home': self.home,
            'edit': self.edit,
            'membros': self.membros,
            'login': self.login,
            'create': self.create,
            'confirma': self.confirma,
            'noticias': self.noticias,
            'produtos': self.produtos,
            'edit_product': self.edit_product,
            'servicos': self.servicos
        }

        self.__users = UserRecord()
        self.__sacola = []

    def home(self):
        return template('app/views/html/home.html')

    def edit(self):
        current_user = self.getCurrentUserBySessionId()
        user_accounts = self.__users.getUserAccounts()
        return template('app/views/html/edit.html', user=current_user, accounts=user_accounts)

    def membros(self):
        self.update_users_list()
        current_user = self.getCurrentUserBySessionId()
        if current_user and current_user.isAdmin():  # Verifica se é admin
            user_accounts = self.__users.getUserAccounts()
            return template('app/views/html/membros_admin', current_user=current_user, users=user_accounts)
        else:
            self.__users.read_products()
            products = self.__users.get_products()
            return template('app/views/html/membros', transfered=True, current_user=current_user, products=products)

    def login(self):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            redirect('/membros')
        return template('app/views/html/login.tpl')

    def process_login(self):
        username = request.forms.get('username')
        password = request.forms.get('password')
        session_id = self.__users.checkUser(username, password)
        
        if session_id:
            response.set_cookie('session_id', session_id, secret='sua-chave-secreta')
            redirect('/membros')
        else:
            return template('app/views/html/login.tpl', error="Credenciais inválidas")

    def create(self):
        return template('app/views/html/create.html')

    def confirma(self):
        return template('app/views/html/confirma.html')

    def noticias(self):
        self.__users.save_products_of_the_day()
        news = self.__users.get_all_news()
        products_file_path = "/static/files/products_of_the_day.json"
        return template('app/views/html/noticias.html', news=news, products_file_path=products_file_path)

    def produtos(self):
        return template('app/views/html/produtos.html')

    def edit_product(self):
        return template('app/views/html/edit_product.html')

    def servicos(self):
        products = self.get_products()
        return template('app/views/html/servicos.html', products=products)

    def review_cart(self):
        total = self.calculate_total()
        return template('app/views/html/review_cart.html', cart_products=self.__sacola, total_price=total)

    def checkout(self):
        total = self.calculate_total()
        return template('app/views/html/checkout.html', cart_products=self.__sacola, total_price=total)

    def generate_invoice(self):
        total = self.calculate_total()
        purchase_note = 'Compra realizada com sucesso!\n'
        purchase_note += f'Total a pagar: R$ {total:.2f}\n{"-"*30}\n'
        for product in self.__sacola:
            purchase_note += f'Produto: {product.name}\n'
            purchase_note += f'Quantidade: {product.quantity}\n'
            purchase_note += f'Preço Unitário: R$ {product.price}\n'
            purchase_note += f'Total: R$ {product.price * product.quantity}\n{"-"*30}\n'

        for product in self.__sacola:
            self.__users.remove_product(product.name)

        self.__sacola = []

        file_path = 'purchase_confirmation.txt'
        with open(file_path, 'w') as file:
            file.write(purchase_note)
        
        response.content_type = 'text/plain'
        response.headers['Content-Disposition'] = f'attachment; filename="{file_path}"'
        return open(file_path, 'r').read()

    def get_product_by_name(self, name):
        """Obtém um produto pelo nome"""
        return self.__users.get_product_by_name(name)

    def add_product(self, name, quantity):
        self.__users.add_product(name, quantity)
        redirect('/membros')

    def edit_product(self, name):
        product = self.__users.get_product_by_name(name)
        if product:
            return template('app/views/html/edit_product', product=product)
        redirect('/membros')

    def update_product(self, old_name, new_name, quant):
        self.__users.update_product(old_name, new_name, quant)

    def remove_product(self, name):
        self.__users.remove_product(name)
        self.removed = f'O produto {name} foi removido com sucesso.'
        redirect('/membros')

    def servicos(self):
        self.__users.read_products()  # Certifica-se de carregar os produtos atualizados
        products = self.__users.get_products()  # Obtém os produtos
        return template('app/views/html/servicos', products=products)  # Renderiza a página de serviços com os produtos

    # Método para o administrador editar a senha de um usuário
    def update_user_password(self, username, new_password):
        self.__users.setUser(username, new_password)
        redirect('/membros')

    # Método para o administrador excluir um usuário
    def delete_user_by_admin(self, username):
        user = self.__users.get_user_by_username(username)
        if user:
            self.__users.removeUser(user)
        redirect('/membros')

    def home(self):
        return template('app/views/html/home')

    def confirma(self):
        return template('app/views/html/confirma')

    def produto(self):
        return template('app/views/html/produto')

    def noticias(self):
        return template('app/views/html/noticias')

    def produtos(self):
        products = self.__users.get_products()
        return template('app/views/html/produtos', products=products)

    def serviços(self):
        return template('app/views/html/serviços')