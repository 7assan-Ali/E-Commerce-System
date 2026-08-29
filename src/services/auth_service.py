class AuthService:
    @staticmethod
    def login(user, email: str, password: str) -> bool:
        return user.email == email and user.password == password
