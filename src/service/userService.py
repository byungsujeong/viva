import bcrypt


class UserService:
    encoding: str = "utf-8"

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            password=password.encode(self.encoding),
            salt=bcrypt.gensalt(),
        )
        return hashed_password.decode(self.encoding)