class UserAccount():

    def __init__(self, username, password):
        self.username= username
        self.password= password
    #     self.profile_image = profile_image  # Novo atributo para armazenar o caminho da imagem de perfil
        
    # def set_profile_image(self, image_path):
    #     self.profile_image = image_path

    # def get_profile_image(self):
    #     return self.profile_image

    def isAdmin(self):
        return False

class SuperAccount(UserAccount):

    def __init__(self, username, password, permissions):

        super().__init__(username, password)
        self.permissions= permissions
        if not permissions:
            self.permissions= ['user']

    def isAdmin(self):
        return True