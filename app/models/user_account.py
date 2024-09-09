class UserAccount:
    def __init__(self, username, password, profile_image=None):
        self.username = username
        self.password = password
        self.profile_image = profile_image  # Novo atributo para armazenar o caminho da imagem de perfil

    def set_profile_image(self, image_path):
        self.profile_image = image_path

    def get_profile_image(self):
        return self.profile_image
