class User:
    def __init__(self, user_id: int, name: str, email: str, password: str, phone: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone

    def login(self) -> bool:
        return True

    def logout(self) -> None:
        pass

    def update_profile(self, name=None, email=None, phone=None) -> None:
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
