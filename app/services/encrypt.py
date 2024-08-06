from passlib.context import CryptContext

__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password(password: str) -> str:
    """
    Хэширует пароль с использованием контекста хэширования паролей.

    :param password: Пароль в виде строки, который нужно захешировать.
    :return: Захешированный пароль в виде строки.
    """
    return __pwd_context.hash(password)


def validate_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли введенный пароль захешированному паролю.

    :param plain_password: Введенный пароль в виде строки.
    :param hashed_password: Захешированный пароль в виде строки, с которым нужно сравнить введенный пароль.
    :return: True, если введенный пароль соответствует захешированному, иначе False.
    """
    return __pwd_context.verify(plain_password, hashed_password)
